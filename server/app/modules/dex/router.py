from app.core.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .schema import DexCreate, DexResponse, DexStats, DexUpdate

router = APIRouter(prefix="/dexs", tags=["dex"])


@router.get("", response_model=list[DexResponse])
async def list_dex(
    category: str | None = None,
    status: str | None = None,
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
):
    return await crud.get_dex(db, category, status, skip, limit)


@router.get("/stats", response_model=DexStats)
async def get_dex_stats(db: AsyncSession = Depends(get_db)):
    return await crud.get_dex_stats(db)


@router.get("/slug/{slug}", response_model=DexResponse)
async def get_dex_by_slug(slug: str, db: AsyncSession = Depends(get_db)):
    entry = await crud.get_dex_by_slug(db, slug)
    if not entry:
        raise HTTPException(status_code=404, detail="图鉴未找到")
    return entry


@router.get("/slug/{slug}/related", response_model=list[DexResponse])
async def get_related_dex(slug: str, db: AsyncSession = Depends(get_db)):
    dex = await crud.get_dex_by_slug(db, slug)
    if not dex:
        raise HTTPException(status_code=404, detail="图鉴未找到")
    related_dexs = await crud.get_related_dexs(db, dex, limit=3)
    return related_dexs


@router.get("/{entry_id}", response_model=DexResponse)
async def get_dex_by_id(entry_id: str, db: AsyncSession = Depends(get_db)):
    entry = await crud.get_dex_by_id(db, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="图鉴未找到")
    return entry


@router.post("", response_model=DexResponse, status_code=201)
async def create_dex(data: DexCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_dex(db, data)


@router.put("/{entry_id}", response_model=DexResponse)
async def update_dex(
    entry_id: str, data: DexUpdate, db: AsyncSession = Depends(get_db)
):
    entry = await crud.get_dex_by_id(db, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="图鉴未找到")
    entry = await crud.update_dex(db, entry, data)
    return entry


@router.delete("/{entry_id}", status_code=204)
async def delete_dex(entry_id: str, db: AsyncSession = Depends(get_db)):
    entry = await crud.get_dex_by_id(db, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="图鉴未找到")
    await crud.delete_dex(db, entry)
