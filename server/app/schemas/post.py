from pydantic import BaseModel, Field

from app.schemas.post_category import PostCategoryResponse
from app.schemas.post_tag import PostTagResponse

# ---------- 创建 / 更新 ----------
class PostCreate(BaseModel):
    slug: str
    title: str
    description: str | None = None
    content: str
    cover_image: str | None = Field(None, alias="coverImage")
    published: bool = False
    featured: bool = False
    category_id: str = Field(..., alias="categoryId")
    tag_ids: list[str] = Field(default_factory=list, alias="tagIds")
    reading_time: int = Field(default=0, alias="readingTime")
    word_count: int = Field(default=0, alias="wordCount")

    model_config = {"populate_by_name": True}


class PostUpdate(BaseModel):
    slug: str | None = None
    title: str | None = None
    description: str | None = None
    content: str | None = None
    cover_image: str | None = Field(None, alias="coverImage")
    published: bool | None = None
    featured: bool | None = None
    category_id: str = Field(..., alias="categoryId")
    tag_ids: list[str] = Field(default_factory=list, alias="tagIds")
    reading_time: int = Field(default=0, alias="readingTime")
    word_count: int = Field(default=0, alias="wordCount")

    model_config = {"populate_by_name": True}

# ---------- 响应 ----------


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
    reading_time: int = Field(default=0, alias="readingTime")
    word_count: int = Field(default=0, alias="wordCount")
    views: int
    featured: bool

    model_config = {"from_attributes": True, "populate_by_name": True}


# ---------- 列表 ----------
class PostListItem(BaseModel):
    id: str
    slug: str
    title: str
    description: str | None = None
    content: str
    cover_image: str | None = Field(None, alias="coverImage")
    created_at: str = Field(..., alias="createdAt")
    updated_at: str = Field(..., alias="updatedAt")
    published: bool
    featured: bool
    category: PostCategoryResponse | None = None
    tags: list[PostTagResponse] = Field(default_factory=list)
    reading_time: int = Field(default=0, alias="readingTime")
    word_count: int = Field(default=0, alias="wordCount")
    views: int

    model_config = {"from_attributes": True, "populate_by_name": True}


# ---------- 归档 ----------
class ArchiveItem(BaseModel):
    year: int
    month: int
    posts: list[PostListItem]
