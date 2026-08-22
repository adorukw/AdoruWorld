"""创建/重置初始管理员账号

用法:
    python -m scripts.create_admin [用户名] [邮箱]

密码来源（优先级）:
    1. .env 的 INITIAL_ADMIN_PASSWORD
    2. 自动生成随机密码并打印（仅此一次，请立即保存）
"""
import asyncio
import secrets

from app.core.config import INITIAL_ADMIN_PASSWORD
from app.core.database import async_session, init_db
from app.core.security import hash_password
from app.modules.user import crud as user_crud


async def main():
    import sys

    username = sys.argv[1] if len(sys.argv) > 1 else "admin"
    email = sys.argv[2] if len(sys.argv) > 2 else "admin@example.com"

    await init_db()

    password = INITIAL_ADMIN_PASSWORD or secrets.token_urlsafe(12)
    generated = not INITIAL_ADMIN_PASSWORD

    async with async_session() as db:
        existing = await user_crud.get_user_by_username(db, username)
        if existing:
            existing.password_hash = hash_password(password)
            existing.role = "admin"
            existing.is_active = True
            existing.email_verified = True
            await db.commit()
            print(f"✅ 管理员 {username} 已存在，密码已重置")
        else:
            await user_crud.create_user(
                db,
                username=username,
                email=email,
                password_hash=hash_password(password),
                role="admin",
                email_verified=True,
            )
            print(f"✅ 管理员 {username} 创建成功")

    if generated:
        print(f"\n🔐 初始密码: {password}\n   （随机生成，仅显示这一次，请立即保存）")


if __name__ == "__main__":
    asyncio.run(main())
