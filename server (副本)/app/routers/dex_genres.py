from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.crud import dex_genres as crud
from app.schemas import DexGenreResponse, DexGenreCreate, DexGenreUpdate

router = APIRouter(prefix="/dex_genres", tags=["dex_genres"])


@router.get("", response_model=list[DexGenreResponse])
async def list_genres(db: AsyncSession = Depends(get_db)):
    rows = await crud.get_genres(db)
    res = []
    for row in rows:
        res.append(DexGenreResponse(
            id=row.id, name=row.name, slug=row.slug, color=row.color,
        ))
    return res


@router.get("/slug/{slug}", response_model=DexGenreResponse)
async def get_genre_by_slug(slug: str, db: AsyncSession = Depends(get_db)):
    genre = await crud.get_genre_by_slug(db, slug)
    if not genre:
        raise HTTPException(status_code=404, detail="题材未找到")
    return DexGenreResponse(
        id=genre.id, name=genre.name, slug=genre.slug, color=genre.color,
    )


@router.get("/{genre_id}", response_model=DexGenreResponse)
async def get_genre_by_id(genre_id: str, db: AsyncSession = Depends(get_db)):
    genre = await crud.get_genre_by_id(db, genre_id)
    if not genre:
        raise HTTPException(status_code=404, detail="题材未找到")
    return DexGenreResponse(
        id=genre.id, name=genre.name, slug=genre.slug, color=genre.color,
    )


@router.post("", response_model=DexGenreResponse, status_code=201)
async def create_genre(data: DexGenreCreate, db: AsyncSession = Depends(get_db)):
    genre = await crud.create_genre(db, data)
    return DexGenreResponse(
        id=genre.id, name=genre.name, slug=genre.slug, color=genre.color,
    )


@router.put("/{genre_id}", response_model=DexGenreResponse)
async def update_genre(genre_id: str, data: DexGenreUpdate, db: AsyncSession = Depends(get_db)):
    genre = await crud.get_genre_by_id(db, genre_id)
    if not genre:
        raise HTTPException(status_code=404, detail="题材未找到")
    genre = await crud.update_genre(db, genre, data)
    return DexGenreResponse(
        id=genre.id, name=genre.name, slug=genre.slug, color=genre.color,
    )


@router.delete("/{genre_id}", status_code=204)
async def delete_genre(genre_id: str, db: AsyncSession = Depends(get_db)):
    genre = await crud.get_genre_by_id(db, genre_id)
    if not genre:
        raise HTTPException(status_code=404, detail="题材未找到")
    await crud.delete_genre(db, genre)
    return None