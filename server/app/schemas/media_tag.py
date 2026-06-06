from pydantic import BaseModel


class MediaTagCreate(BaseModel):
    name: str
    slug: str
    color: str | None = None


class MediaTagUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None
    color: str | None = None


class MediaTagResponse(BaseModel):
    id: str
    name: str
    slug: str
    color: str | None = None

    model_config = {"from_attributes": True}
