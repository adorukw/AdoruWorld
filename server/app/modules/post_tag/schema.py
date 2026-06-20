from pydantic import BaseModel


class PostTagCreate(BaseModel):
    name: str
    slug: str
    color: str | None = None


class PostTagUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None
    color: str | None = None


class PostTagResponse(BaseModel):
    id: str
    count: int = 0

    name: str
    slug: str
    color: str | None = None

    model_config = {"from_attributes": True}
