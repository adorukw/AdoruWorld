"""认证路由：注册 → 邮箱验证 → 登录 → token 刷新/登出

安全设计：
- 登录失败统一报"用户名或密码错误"，防用户名枚举
- 登录连续失败 5 次锁 15 分钟（内存限流）
- refresh token 轮换：每次刷新作废旧 refresh、签发新的（防 token 被盗长期滥用）
"""
import hashlib
from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.mailer import send_verification_email
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    generate_verification_code,
    hash_password,
    hash_refresh_token,
    verify_password,
)
from app.modules.auth import limiter
from app.modules.auth.dependency import get_current_user
from app.modules.user import crud as user_crud
from app.modules.user.model import User
from app.modules.user.schema import TokenResponse, UserResponse

import jwt as pyjwt

router = APIRouter(prefix="/auth", tags=["auth"])


# ============================================================
# 请求模型
# ============================================================

class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)


class VerifyEmailRequest(BaseModel):
    email: EmailStr
    code: str = Field(min_length=6, max_length=6)


class LoginRequest(BaseModel):
    # 支持用户名或邮箱登录
    account: str
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str = Field(..., alias="refreshToken")

    model_config = {"populate_by_name": True}


# ============================================================
# 注册 + 邮箱验证
# ============================================================

@router.post("/register", status_code=201)
async def register(data: RegisterRequest, db: Annotated[AsyncSession, Depends(get_db)]):
    # 注册不暴露"用户名已存在"还是"邮箱已存在"，统一报注册失败
    if await user_crud.get_user_by_username(db, data.username):
        raise HTTPException(status_code=409, detail="注册失败，请检查填写的信息")
    if await user_crud.get_user_by_email(db, data.email):
        raise HTTPException(status_code=409, detail="注册失败，请检查填写的信息")

    user = await user_crud.create_user(
        db,
        username=data.username,
        email=data.email,
        password_hash=hash_password(data.password),
        role="viewer",  # 开放注册，但默认只读，写权限由管理员分配
    )

    await _issue_verification_code(db, user)
    return {"message": "注册成功，验证码已发送至邮箱"}


async def _issue_verification_code(db: AsyncSession, user: User) -> None:
    code = generate_verification_code()
    code_hash = hashlib.sha256(code.encode()).hexdigest()
    await user_crud.create_email_verification(db, user.id, code_hash)
    await send_verification_email(user.email, code)


@router.post("/verify-email")
async def verify_email(
    data: VerifyEmailRequest, db: Annotated[AsyncSession, Depends(get_db)]
):
    user = await user_crud.get_user_by_email(db, data.email)
    if not user or user.email_verified:
        # 已验证/不存在都报同样的错，不给探测空间
        raise HTTPException(status_code=400, detail="验证失败")

    record = await user_crud.get_active_verification(db, user.id)
    if record is None:
        raise HTTPException(status_code=400, detail="验证码已过期，请重新获取")

    if record.attempts >= limiter.VERIFY_MAX_ATTEMPTS:
        raise HTTPException(status_code=429, detail="尝试次数过多，请重新获取验证码")

    if hashlib.sha256(data.code.encode()).hexdigest() != record.code_hash:
        record.attempts += 1
        await db.commit()
        raise HTTPException(status_code=400, detail="验证码错误")

    record.used = True
    user.email_verified = True
    await db.commit()
    return {"message": "邮箱验证成功，现在可以登录了"}


@router.post("/resend-code")
async def resend_code(
    data: VerifyEmailRequest, db: Annotated[AsyncSession, Depends(get_db)]
):
    user = await user_crud.get_user_by_email(db, data.email)
    if not user or user.email_verified:
        # 静默成功，不暴露邮箱是否注册过
        return {"message": "如果该邮箱需要验证，验证码已发送"}

    if not limiter.check_send_interval(user.email):
        raise HTTPException(status_code=429, detail="发送过于频繁，请 1 分钟后再试")

    await _issue_verification_code(db, user)
    return {"message": "验证码已重新发送"}


# ============================================================
# 登录 / 刷新 / 登出 / 当前用户
# ============================================================

@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: Annotated[AsyncSession, Depends(get_db)]):
    if limiter.is_locked(f"login:{data.account}", limiter.LOGIN_MAX_FAILS, limiter.LOGIN_LOCK_SECONDS):
        raise HTTPException(status_code=429, detail="失败次数过多，请 15 分钟后再试")

    user = await user_crud.get_user_by_username(db, data.account) or \
        await user_crud.get_user_by_email(db, data.account)

    if user is None or not verify_password(data.password, user.password_hash):
        limiter.record_fail(f"login:{data.account}")
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="账号已被禁用")
    if not user.email_verified:
        raise HTTPException(status_code=403, detail="请先完成邮箱验证")

    limiter.reset(f"login:{data.account}")
    await user_crud.touch_last_login(db, user)

    return await _issue_token_pair(db, user)


async def _issue_token_pair(db: AsyncSession, user: User) -> TokenResponse:
    access = create_access_token(user.id, user.role)
    refresh = create_refresh_token(user.id, user.role)
    # refresh 落库（存摘要），登出/禁用时可吊销
    payload = decode_token(refresh, expected_type="refresh")
    await user_crud.store_refresh_token(
        db, user.id, hash_refresh_token(refresh),
        expires_at=datetime.fromtimestamp(payload["exp"], tz=timezone.utc),
    )
    return TokenResponse(
        access_token=access, refresh_token=refresh, user=user,
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_tokens(
    data: RefreshRequest, db: Annotated[AsyncSession, Depends(get_db)]
):
    try:
        payload = decode_token(data.refresh_token, expected_type="refresh")
    except pyjwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="登录已过期，请重新登录")
    except pyjwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="无效的凭证")

    token_hash = hash_refresh_token(data.refresh_token)
    record = await user_crud.find_refresh_token(db, token_hash)
    if record is None or record.revoked:
        raise HTTPException(status_code=401, detail="凭证已失效，请重新登录")

    user = await user_crud.get_user_by_id(db, payload["sub"])
    if user is None or not user.is_active:
        raise HTTPException(status_code=401, detail="账号不可用")

    # 轮换：旧 refresh 立即作废，签发全新一对
    await user_crud.revoke_refresh_token(db, token_hash)
    return await _issue_token_pair(db, user)


@router.post("/logout")
async def logout(
    data: RefreshRequest, db: Annotated[AsyncSession, Depends(get_db)]
):
    # JWT 是无状态的，登出 = 吊销 refresh；access 短期内自然过期
    await user_crud.revoke_refresh_token(db, hash_refresh_token(data.refresh_token))
    return {"message": "已登出"}


@router.get("/me", response_model=UserResponse)
async def read_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
