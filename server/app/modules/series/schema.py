from pydantic import BaseModel, Field


class SeriesCreate(BaseModel):
    name: str
    slug: str
    description: str | None = None
    cover_image: str | None = Field(None, alias="coverImage")

    model_config = {"populate_by_name": True}


class SeriesUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None
    description: str | None = None
    cover_image: str | None = Field(None, alias="coverImage")

    model_config = {"populate_by_name": True}


class SeriesResponse(BaseModel):
    id: str
    count: int = 0

    name: str
    slug: str
    description: str | None = None
    cover_image: str | None = Field(None, alias="coverImage")

    model_config = {"from_attributes": True, "populate_by_name": True}


class SeriesPostResponse(BaseModel):
    """系列文章列表用的轻量版，不含 content，附系列内序号"""

    id: str
    slug: str
    title: str
    description: str | None = None
    cover_image: str | None = Field(None, alias="coverImage")
    created_at: str = Field(..., alias="createdAt")
    updated_at: str = Field(..., alias="updatedAt")
    published: bool
    reading_time: int = Field(default=0, alias="readingTime")
    word_count: int = Field(default=0, alias="wordCount")
    views: int
    featured: bool
    series_order: int | None = Field(None, alias="seriesOrder")

    model_config = {"from_attributes": True, "populate_by_name": True}
