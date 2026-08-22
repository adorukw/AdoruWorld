"""认证安全工具：密码哈希、JWT 签发校验、邮箱验证码生成

设计要点：
- bcrypt 自带随机盐，同一密码每次哈希结果不同，校验用 checkpw
- JWT payload 只放最小必要信息（sub/role/type/exp），JWT 是签名不是加密
- refresh token 存库时只存 sha256 摘要，泄库也不会泄露可用 token
"""
import hashlib
import secrets
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.core.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
    SECRET_KEY,
)

JWT_ALGORITHM = "HS256"


# ============================================================
# 密码哈希
# ============================================================

def hash_password(password: str) -> str:
    """bcrypt 哈希，cost factor 默认 12（2^12 轮，约 250ms/次）"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except ValueError:
        return False


# ============================================================
# JWT
# ============================================================

def _create_token(user_id: str, role: str, token_type: str, expires_delta: timedelta) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,
        "role": role,
        "type": token_type,
        # jti(JWT ID)：保证同一秒签发的多个 token 也互不相同，
        # 否则同秒重复登录会产生完全相同的 token
        "jti": secrets.token_hex(8),
        "iat": now,
        "exp": now + expires_delta,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)


def create_access_token(user_id: str, role: str) -> str:
    return _create_token(
        user_id, role, "access",
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )


def create_refresh_token(user_id: str, role: str) -> str:
    return _create_token(
        user_id, role, "refresh",
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    )


def decode_token(token: str, expected_type: str) -> dict:
    """解码并校验签名、过期时间、token 类型；不合法抛 jwt.InvalidTokenError 系异常"""
    payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
    if payload.get("type") != expected_type:
        raise jwt.InvalidTokenError(f"期望 {expected_type} token")
    return payload


def hash_refresh_token(token: str) -> str:
    """refresh token 落库摘要（存原文等于给了钥匙）"""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


# ============================================================
# 邮箱验证码
# ============================================================

def generate_verification_code() -> str:
    """6 位数字验证码，secrets 比 random 更防预测"""
    return f"{secrets.randbelow(1000000):06d}"
