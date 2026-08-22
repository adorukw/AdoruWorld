from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

VALID_ROLES = ("admin", "editor", "viewer")


class UserResponse(BaseModel):
    """注意：没有 password_hash —— 密码哈希永不离开服务端"""

    id: str
    username: str
    email: EmailStr
    role: str
    is_active: bool
    email_verified: bool
    display_name: str | None = None
    avatar: str | None = None
    bio: str | None = None
    created_at: datetime
    last_login_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    """管理员更新用户：改角色 / 启停 / 展示信息"""

    role: str | None = None
    is_active: bool | None = None
    display_name: str | None = None
    bio: str | None = None


class TokenResponse(BaseModel):
    access_token: str = Field(..., alias="accessToken")
    refresh_token: str = Field(..., alias="refreshToken")
    token_type: str = Field("bearer", alias="tokenType")
    user: UserResponse

    model_config = ConfigDict(populate_by_name=True)
