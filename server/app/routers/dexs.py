from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.crud import dexs as crud
from app.schemas import DexEntryResponse, DexEntryCreate, DexEntryUpdate, DexStats, DexCategoryInfo, DexStatusInfo

router = APIRouter(prefix="/dexs", tags=["dex"])

# DEX_CATEGORIES: list[DexCategoryInfo] = [
#     DexCategoryInfo(id="anime", name="动漫", slug="anime",
#                     icon="📺", color="#E91E63", bgColor="#FCE4EC"),
#     DexCategoryInfo(id="movie", name="电影", slug="movie",
#                     icon="🎬", color="#9C27B0", bgColor="#F3E5F5"),
#     DexCategoryInfo(id="tv", name="剧集", slug="tv",  icon="📡",
#                     color="#2196F3", bgColor="#E0F7FD"),
#     DexCategoryInfo(id="game", name="游戏", slug="game",
#                     icon="🎮", color="#4CAF50", bgColor="#E8F5E9"),
#     DexCategoryInfo(id="book", name="书籍", slug="book",
#                     icon="📖", color="#FF9800", bgColor="#FFF3E0"),
#     DexCategoryInfo(id="music", name="音乐", slug="music",
#                     icon="🎵", color="#00BCD4", bgColor="#E0F7FA"),
#     DexCategoryInfo(id="other", name="其他", slug="other",
#                     icon="❓", color="#607D8B", bgColor="#ECEFF1"),
# ]

# DEX_STATUSES: list[DexStatusInfo] = [
#     DexStatusInfo(id="completed", name="已完成",
#                   slug="completed", icon="✅", color="#4CAF50"),
#     DexStatusInfo(id="watching", name="在看", slug="watching",
#                   icon="👀", color="#2196F3"),
#     DexStatusInfo(id="playing", name="在玩", slug="playing",
#                   icon="🎮", color="#FF9800"),
#     DexStatusInfo(id="reading", name="在读", slug="reading",
#                   icon="📖", color="#9C27B0"),
#     DexStatusInfo(id="listening", name="在听", slug="listening",
#                   icon="🎧", color="#00BCD4"),
#     DexStatusInfo(id="dropped", name="搁置", slug="dropped",
#                   icon="❌", color="#F44336"),
#     DexStatusInfo(id="planned", name="计划", slug="planned",
#                   icon="📋", color="#607D8B"),
# ]


# @router.get("/categories", response_model=list[DexCategoryInfo])
# async def list_dex_categories():
#     return DEX_CATEGORIES


# @router.get("/statuses", response_model=list[DexStatusInfo])
# async def list_dex_statuses():
#     return DEX_STATUSES

@router.get("", response_model=list[DexEntryResponse])
async def list_dex_entries(
    category: str | None = None,
    status: str | None = None,
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db)
):
    return await crud.get_dex_entries(db, category, status, skip, limit)


@router.get("/stats", response_model=DexStats)
async def get_dex_stats(db: AsyncSession = Depends(get_db)):
    return await crud.get_dex_stats(db)


@router.get("/slug/{slug}", response_model=DexEntryResponse)
async def get_dex_entry_by_slug(slug: str, db: AsyncSession = Depends(get_db)):
    entry = await crud.get_dex_entry_by_slug(db, slug)
    if not entry:
        raise HTTPException(status_code=404, detail="图鉴未找到")
    return entry


@router.get("/{entry_id}", response_model=DexEntryResponse)
async def get_dex_entry_by_id(entry_id: str, db: AsyncSession = Depends(get_db)):
    entry = await crud.get_dex_entry_by_id(db, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="图鉴未找到")
    return entry


@router.post("", response_model=DexEntryResponse, status_code=201)
async def create_dex_entry(data: DexEntryCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_dex_entry(db, data)


@router.put("/{entry_id}", response_model=DexEntryResponse)
async def update_dex_entry(entry_id: str, data: DexEntryUpdate, db: AsyncSession = Depends(get_db)):
    entry = await crud.get_dex_entry_by_id(db, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="图鉴未找到")
    entry = await crud.update_dex_entry(db, entry, data)
    return entry


@router.delete("/{entry_id}", status_code=204)
async def delete_dex_entry(entry_id: str, db: AsyncSession = Depends(get_db)):
    entry = await crud.get_dex_entry_by_id(db, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="图鉴未找到")
    await crud.delete_dex_entry(db, entry)
