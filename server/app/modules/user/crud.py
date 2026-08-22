from datetime import datetime, timedelta, timezone

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .model import EmailVerification, RefreshToken, User


async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    res = await db.execute(select(User).where(User.username == username))
    return res.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    res = await db.execute(select(User).where(User.email == email))
    return res.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: str) -> User | None:
    res = await db.execute(select(User).where(User.id == user_id))
    return res.scalar_one_or_none()


async def get_users(db: AsyncSession) -> list[User]:
    res = await db.execute(select(User).order_by(User.created_at))
    return list(res.scalars().all())


async def create_user(
    db: AsyncSession,
    username: str,
    email: str,
    password_hash: str,
    role: str = "viewer",
    email_verified: bool = False,
) -> User:
    user = User(
        username=username,
        email=email,
        password_hash=password_hash,
        role=role,
        email_verified=email_verified,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def touch_last_login(db: AsyncSession, user: User) -> None:
    user.last_login_at = datetime.now(timezone.utc)
    await db.commit()


# ============================================================
# 邮箱验证码
# ============================================================

async def create_email_verification(
    db: AsyncSession, user_id: str, code_hash: str, ttl_minutes: int = 10
) -> EmailVerification:
    # 作废该用户所有旧验证码，一人同时只有一个有效码
    await db.execute(
        update(EmailVerification)
        .where(EmailVerification.user_id == user_id)
        .values(used=True)
    )
    record = EmailVerification(
        user_id=user_id,
        code_hash=code_hash,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=ttl_minutes),
    )
    db.add(record)
    await db.commit()
    return record


async def get_active_verification(
    db: AsyncSession, user_id: str
) -> EmailVerification | None:
    res = await db.execute(
        select(EmailVerification)
        .where(
            EmailVerification.user_id == user_id,
            EmailVerification.used == False,  # noqa: E712
            EmailVerification.expires_at > datetime.now(timezone.utc),
        )
        .order_by(EmailVerification.created_at.desc())
        .limit(1)
    )
    return res.scalar_one_or_none()


# ============================================================
# refresh token 白名单
# ============================================================

async def store_refresh_token(
    db: AsyncSession, user_id: str, token_hash: str, expires_at: datetime
) -> None:
    db.add(RefreshToken(user_id=user_id, token_hash=token_hash, expires_at=expires_at))
    await db.commit()


async def find_refresh_token(db: AsyncSession, token_hash: str) -> RefreshToken | None:
    res = await db.execute(
        select(RefreshToken).where(RefreshToken.token_hash == token_hash)
    )
    return res.scalar_one_or_none()


async def revoke_refresh_token(db: AsyncSession, token_hash: str) -> None:
    await db.execute(
        update(RefreshToken)
        .where(RefreshToken.token_hash == token_hash)
        .values(revoked=True)
    )
    await db.commit()


async def revoke_all_user_tokens(db: AsyncSession, user_id: str) -> None:
    """禁用用户 / 改角色时调用：踢掉该用户所有在线会话"""
    await db.execute(
        update(RefreshToken)
        .where(RefreshToken.user_id == user_id)
        .values(revoked=True)
    )
    await db.commit()


async def cleanup_expired_tokens(db: AsyncSession) -> int:
    """定期清理过期 token 行（可在迁移或运维脚本里调用）"""
    res = await db.execute(
        delete(RefreshToken).where(
            RefreshToken.expires_at < datetime.now(timezone.utc)
        )
    )
    await db.commit()
    return res.rowcount
