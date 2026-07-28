from typing import Annotated

from app.core.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .schema import MediaTagCreate, MediaTagResponse, MediaTagUpdate

router = APIRouter(prefix="/media_tags", tags=["media_tags"])


@router.get("", response_model=list[MediaTagResponse])
async def list_tags(db: Annotated[AsyncSession, Depends(get_db)]):
    rows = await crud.get_tags(db)
    res = []
    for row in rows:
        res.append(
            MediaTagResponse(id=row.id, name=row.name, slug=row.slug, color=row.color)
        )
    return res


@router.get("/slug/{slug}", response_model=MediaTagResponse)
async def get_tag_by_slug(slug: str, db: Annotated[AsyncSession, Depends(get_db)]):
    tag = await crud.get_tag_by_slug(db, slug)
    if not tag:
        raise HTTPException(status_code=404, detail="标签未找到")
    return MediaTagResponse(id=tag.id, name=tag.name, slug=tag.slug, color=tag.color)


@router.get("/{id}", response_model=MediaTagResponse)
async def get_tag_by_id(id: str, db: Annotated[AsyncSession, Depends(get_db)]):
    tag = await crud.get_tag_by_id(db, id)
    if not tag:
        raise HTTPException(status_code=404, detail="标签未找到")
    return MediaTagResponse(id=tag.id, name=tag.name, slug=tag.slug, color=tag.color)


@router.post("", response_model=MediaTagResponse)
async def create_tag(
    data: MediaTagCreate, db: Annotated[AsyncSession, Depends(get_db)]
):
    tag = await crud.create_tag(db, data)
    return MediaTagResponse(id=tag.id, name=tag.name, slug=tag.slug, color=tag.color)


@router.put("/{tag_id}", response_model=MediaTagResponse)
async def update_tag(
    tag_id: str, data: MediaTagUpdate, db: Annotated[AsyncSession, Depends(get_db)]
):
    tag = await crud.get_tag_by_id(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="标签未找到")
    tag = await crud.update_tag(db, tag, data)
    return MediaTagResponse(id=tag.id, name=tag.name, slug=tag.slug, color=tag.color)


@router.delete("/{tag_id}", status_code=204)
async def delete_tag(tag_id: str, db: Annotated[AsyncSession, Depends(get_db)]):
    tag = await crud.get_tag_by_id(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="标签未找到")
    await crud.delete_tag(db, tag)
