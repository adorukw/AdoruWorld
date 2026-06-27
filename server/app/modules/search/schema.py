from pydantic import BaseModel, Field


class SearchResultItem(BaseModel):
    """搜索结果的统一条目格式。"""
    id: str
    type: str  # "post" | "dex" | "media"
    title: str
    slug: str
    description: str | None = None
    cover_image: str | None = Field(None, alias="coverImage")
    created_at: str | None = Field(None, alias="createdAt")
    matched_fields: list[str] = Field(
        default_factory=list, alias="matchedFields")
    entity_data: dict = Field(default_factory=dict, alias="entityData")

    model_config = {"populate_by_name": True, "from_attributes": True}


class SearchResponse(BaseModel):
    items: list[SearchResultItem]
    total: int
    skip: int
    limit: int
