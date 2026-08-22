from app.modules.post_category.schema import PostCategoryResponse
from app.modules.post_tag.schema import PostTagResponse
from app.modules.series.schema import SeriesResponse
from pydantic import BaseModel, Field, model_validator


def _clean_series_fields(data: dict) -> dict:
    """表单里未选系列时传的是空字符串，统一转成 None 并清掉无意义的序号；
    序号输入框清空时传的也是空字符串，一并转成 None；
    请求里完全不带该字段时不动，避免部分更新误把文章移出系列"""
    sid = "seriesId" if "seriesId" in data else "series_id"
    order_keys = ("seriesOrder", "series_order")
    if sid in data and not data[sid]:
        data[sid] = None
        for key in order_keys:
            if key in data:
                data[key] = None
    else:
        for key in order_keys:
            if key in data and data[key] == "":
                data[key] = None
    return data


class PostCreate(BaseModel):
    title: str
    slug: str
    description: str | None = None
    content: str
    cover_image: str | None = Field(None, alias="coverImage")
    published: bool = False
    featured: bool = False
    category_id: str = Field(..., alias="categoryId")
    tag_ids: list[str] = Field(default_factory=list, alias="tagIds")
    series_id: str | None = Field(None, alias="seriesId")
    series_order: int | None = Field(None, alias="seriesOrder")

    model_config = {"populate_by_name": True}

    @model_validator(mode="before")
    @classmethod
    def clean_series(cls, data):
        return _clean_series_fields(data) if isinstance(data, dict) else data


class PostUpdate(BaseModel):
    slug: str | None = None
    title: str | None = None
    description: str | None = None
    content: str | None = None
    cover_image: str | None = Field(None, alias="coverImage")
    published: bool | None = None
    featured: bool | None = None
    category_id: str | None = Field(..., alias="categoryId")
    tag_ids: list[str] | None = Field(default_factory=list, alias="tagIds")
    series_id: str | None = Field(None, alias="seriesId")
    series_order: int | None = Field(None, alias="seriesOrder")

    model_config = {"populate_by_name": True}

    @model_validator(mode="before")
    @classmethod
    def clean_series(cls, data):
        return _clean_series_fields(data) if isinstance(data, dict) else data


class PostLink(BaseModel):
    """系列内上下篇导航用的极简引用"""

    slug: str
    title: str

    model_config = {"from_attributes": True}


class PostResponse(BaseModel):
    id: str
    slug: str
    title: str
    description: str | None = None
    content: str
    cover_image: str | None = Field(None, alias="coverImage")
    created_at: str = Field(..., alias="createdAt")
    updated_at: str = Field(..., alias="updatedAt")
    published: bool
    category: PostCategoryResponse | None = None
    tags: list[PostTagResponse] = Field(default_factory=list)
    series: SeriesResponse | None = None
    series_order: int | None = Field(None, alias="seriesOrder")
    prev_post: PostLink | None = Field(None, alias="prevPost")
    next_post: PostLink | None = Field(None, alias="nextPost")
    reading_time: int = Field(default=0, alias="readingTime")
    word_count: int = Field(default=0, alias="wordCount")
    views: int
    featured: bool

    model_config = {"from_attributes": True, "populate_by_name": True}


class PostArchiveResponse(BaseModel):
    """归档列表用的轻量版，不含 content"""

    id: str
    slug: str
    title: str
    description: str | None = None
    cover_image: str | None = Field(None, alias="coverImage")
    created_at: str = Field(..., alias="createdAt")
    updated_at: str = Field(..., alias="updatedAt")
    published: bool
    category: PostCategoryResponse | None = None
    tags: list[PostTagResponse] = Field(default_factory=list)
    reading_time: int = Field(default=0, alias="readingTime")
    word_count: int = Field(default=0, alias="wordCount")
    views: int
    featured: bool

    model_config = {"from_attributes": True, "populate_by_name": True}


class ArchiveItem(BaseModel):
    year: int
    month: int
    posts: list[PostArchiveResponse]
