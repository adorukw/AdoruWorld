from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import DexGenre, dex_to_dex_genres
from app.schemas import DexGenreCreate, DexGenreUpdate


async def get_genres(db: AsyncSession) -> list[DexGenre]:
    res = await db.execute(select(DexGenre))
    return list(res.scalars().all())


async def get_genre_by_slug(db: AsyncSession, slug: str) -> DexGenre | None:
    res = await db.execute(select(DexGenre).where(DexGenre.slug == slug))
    return res.scalar_one_or_none()


async def get_genre_by_id(db: AsyncSession, genre_id: str) -> DexGenre | None:
    res = await db.execute(select(DexGenre).where(DexGenre.id == genre_id))
    return res.scalar_one_or_none()


async def create_genre(db: AsyncSession, data: DexGenreCreate) -> DexGenre:
    genre = DexGenre(**data.model_dump())
    db.add(genre)
    await db.commit()
    await db.refresh(genre)
    return genre


async def update_genre(db: AsyncSession, genre: DexGenre, data: DexGenreUpdate) -> DexGenre:
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(genre, key, value)
    await db.commit()
    await db.refresh(genre)
    return genre


async def delete_genre(db: AsyncSession, genre: DexGenre) -> None:
    await db.delete(genre)
    await db.commit()
