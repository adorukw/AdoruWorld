"""用户管理（仅 admin）：列表 / 改角色 / 启停 / 删除"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.auth.dependency import require_role
from app.modules.user import crud as user_crud
from app.modules.user.model import User
from app.modules.user.schema import VALID_ROLES, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])

# 守卫挂在整个 router 上：本模块所有接口都要求 admin
AdminUser = Annotated[User, Depends(require_role("admin"))]


async def _get_user_or_404(db: AsyncSession, user_id: str) -> User:
    user = await user_crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


@router.get("", response_model=list[UserResponse])
async def list_users(db: Annotated[AsyncSession, Depends(get_db)], _: AdminUser):
    return await user_crud.get_users(db)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    data: UserUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    admin: AdminUser,
):
    user = await _get_user_or_404(db, user_id)
    update_data = data.model_dump(exclude_unset=True)

    if "role" in update_data:
        if update_data["role"] not in VALID_ROLES:
            raise HTTPException(status_code=400, detail=f"角色必须是 {VALID_ROLES} 之一")
        # 防止把自己降级导致站点无管理员
        if user.id == admin.id and update_data["role"] != "admin":
            raise HTTPException(status_code=400, detail="不能降级自己的管理员角色")

    for key, value in update_data.items():
        setattr(user, key, value)
    await db.commit()
    await db.refresh(user)

    # 改角色/禁用后踢掉该用户所有会话，权限立即生效
    if "role" in update_data or "is_active" in update_data:
        await user_crud.revoke_all_user_tokens(db, user.id)
    return user


@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    admin: AdminUser,
):
    user = await _get_user_or_404(db, user_id)
    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="不能删除自己")
    if user.role == "admin":
        admins = [u for u in await user_crud.get_users(db) if u.role == "admin"]
        if len(admins) <= 1:
            raise HTTPException(status_code=400, detail="不能删除最后一个管理员")
    await db.delete(user)
    await db.commit()
