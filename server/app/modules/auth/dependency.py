"""认证依赖：JWT 解析 → 查库校验 → 角色守卫

安全边界在后端：前端路由守卫只是体验优化，这里的 Depends 才是真正的门
"""
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import decode_token
from app.modules.user import crud as user_crud
from app.modules.user.model import User

# auto_error=False：未带 token 的请求也进入依赖，由我们统一抛 401
# （否则公共接口挂这个依赖会直接 403）
_bearer = HTTPBearer(auto_error=False)


async def get_current_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
) -> User:
    if credentials is None:
        raise HTTPException(status_code=401, detail="未登录")

    try:
        payload = decode_token(credentials.credentials, expected_type="access")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="登录已过期")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="无效的凭证")

    user = await user_crud.get_user_by_id(db, payload["sub"])
    if user is None or not user.is_active:
        raise HTTPException(status_code=401, detail="账号不存在或已被禁用")
    return user


def require_role(*roles: str):
    """守卫工厂：require_role('admin', 'editor') 生成一个依赖"""

    async def checker(user: User = Depends(get_current_user)) -> User:
        if user.role not in roles:
            raise HTTPException(status_code=403, detail="权限不足")
        return user

    return checker
