from pydantic import BaseModel


class DexGenreCreate(BaseModel):
    name: str
    slug: str
    color: str | None = None


class DexGenreUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None
    color: str | None = None


class DexGenreResponse(BaseModel):
    id: str
    name: str
    slug: str
    color: str | None = None

    model_config = {"from_attributes": True}
