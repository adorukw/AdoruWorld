from pydantic import BaseModel


class PostCategoryCreate(BaseModel):
    name: str
    slug: str
    description: str | None = None
    icon: str | None = None
    color: str | None = None


class PostCategoryUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None
    description: str | None = None
    icon: str | None = None
    color: str | None = None


class PostCategoryResponse(BaseModel):
    id: str
    count: int = 0

    name: str
    slug: str
    description: str | None = None
    icon: str | None = None
    color: str | None = None

    model_config = {"from_attributes": True}
