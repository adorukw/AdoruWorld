from typing import Annotated

from app.core.database import get_db
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .schema import SearchResponse

router = APIRouter(prefix="/search", tags=["search"])


@router.get("", response_model=SearchResponse)
async def global_search(
    db: Annotated[AsyncSession, Depends(get_db)],
    q: str = Query(
        ..., min_length=1, description="搜索关键词，空格或逗号分隔多个词（AND 逻辑）"
    ),
    type: str | None = Query(
        None,
        alias="type",
        regex="^(post|dex|media)$",
        description="筛选实体类型：post / dex / media，不传则搜全部",
    ),
    skip: int = Query(0, ge=0, description="分页偏移"),
    limit: int = Query(20, ge=1, le=100, description="每页条数"),
):
    items, total = await crud.search_all(
        db, q=q, entity_type=type, skip=skip, limit=limit
    )
    return SearchResponse(items=items, total=total, skip=skip, limit=limit)
