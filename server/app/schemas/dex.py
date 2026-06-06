from pydantic import BaseModel, Field

from app.schemas.dex_genre import DexGenreResponse

DexCategoryType = str
DexStatusType = str


class DexEntryCreate(BaseModel):
    slug: str
    title: str
    original_title: str | None = Field(None, alias="originalTitle")
    cover_image: str = Field(..., alias="coverImage")
    category: DexCategoryType
    status: DexStatusType
    rating: float = 0.0
    start_date: str | None = Field(None, alias="startDate")
    finish_date: str | None = Field(None, alias="finishDate")
    comment: str | None = None
    summary: str | None = None
    creator: str | None = None
    year: int | None = None
    genre_ids: list[str] = Field(default_factory=list, alias="genreIds")

    model_config = {"populate_by_name": True}


class DexEntryUpdate(BaseModel):
    slug: str | None = None
    title: str | None = None
    original_title: str | None = Field(None, alias="originalTitle")
    cover_image: str = Field(..., alias="coverImage")
    category: DexCategoryType | None = None
    status: DexStatusType | None = None
    rating: float | None = None
    start_date: str | None = Field(None, alias="startDate")
    finish_date: str | None = Field(None, alias="finishDate")
    comment: str | None = None
    creator: str | None = None
    year: int | None = None
    genre_ids: list[str] | None = Field(None, alias="genreIds")

    model_config = {"populate_by_name": True}


class DexEntryResponse(BaseModel):
    id: str
    slug: str
    title: str
    original_title: str | None = Field(None, alias="originalTitle")
    cover_image: str = Field(..., alias="coverImage")
    category: DexCategoryType
    status: DexStatusType
    rating: float = 0.0
    start_date: str | None = Field(None, alias="startDate")
    finish_date: str | None = Field(None, alias="finishDate")
    comment: str | None = None
    summary: str | None = None
    creator: str | None = None
    year: int | None = None
    genres: list[DexGenreResponse] = Field(default_factory=list)

    model_config = {"from_attributes": True, "populate_by_name": True}


class DexCategoryInfo(BaseModel):
    id: str
    name: str
    slug: str
    icon: str
    color: str
    bgColor: str


class DexStatusInfo(BaseModel):
    id: str
    name: str
    slug: str
    icon: str
    color: str


class DexStats(BaseModel):
    total: int
    byCategory: dict[str, int]
    byStatus: dict[str, int]
    averageRating: float
