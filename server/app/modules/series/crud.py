from app.modules.post.model import Post
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .model import Series
from .schema import SeriesCreate, SeriesUpdate


async def get_series_list(db: AsyncSession) -> list[Series]:
    res = await db.execute(select(Series).order_by(Series.name))
    return list(res.scalars().all())


async def get_series_by_slug(db: AsyncSession, slug: str) -> Series | None:
    res = await db.execute(select(Series).where(Series.slug == slug))
    return res.scalar_one_or_none()


async def get_series_by_id(db: AsyncSession, id: str) -> Series | None:
    res = await db.execute(select(Series).where(Series.id == id))
    return res.scalar_one_or_none()


async def create_series(db: AsyncSession, data: SeriesCreate) -> Series:
    series = Series(**data.model_dump())
    db.add(series)
    await db.commit()
    await db.refresh(series)
    return series


async def update_series(db: AsyncSession, series: Series, data: SeriesUpdate) -> Series:
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(series, key, value)
    await db.commit()
    await db.refresh(series)
    return series


async def delete_series(db: AsyncSession, series: Series) -> None:
    # 引擎未开启 SQLite 外键强制，建表时的 ondelete 不会执行，
    # 删除系列前需显式解除文章关联（文章保留，仅脱离系列）
    await db.execute(
        update(Post).where(Post.series_id == series.id).values(series_id=None)
    )
    await db.delete(series)
    await db.commit()


async def get_series_count(db: AsyncSession, series_id: str) -> int:
    stmt = select(func.count(Post.id)).where(Post.series_id == series_id)
    result = await db.execute(stmt)
    return result.scalar() or 0


async def get_series_posts(
    db: AsyncSession, series_id: str, published_only: bool = False
) -> list[Post]:
    """按系列内序号排序，序号为空或重复时按创建时间兜底"""
    stmt = select(Post).where(Post.series_id == series_id)
    if published_only:
        stmt = stmt.where(Post.published == True)  # noqa: E712
    stmt = stmt.order_by(
        Post.series_order.asc().nulls_last(), Post.created_at.asc()
    )
    res = await db.execute(stmt)
    return list(res.scalars().all())
