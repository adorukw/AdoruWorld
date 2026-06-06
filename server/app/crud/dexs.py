from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import DexEntry, DexGenre
from app.schemas import DexEntryCreate, DexEntryUpdate


async def get_dex_entries(
        db: AsyncSession,
        category: str | None = None,
        status: str | None = None,
        skip: int = 0,
        limit: int = 20
) -> list[DexEntry]:
    stmt = select(DexEntry)
    if category:
        stmt = stmt.where(DexEntry.category == category)
    if status:
        stmt = stmt.where(DexEntry.status == status)
    stmt = stmt.order_by(DexEntry.title).offset(skip).limit(limit)
    res = await db.execute(stmt)
    return list(res.scalars().all())


async def get_dex_stats(db: AsyncSession) -> dict:
    total_res = await db.execute(select(func.count()).select_from(DexEntry))
    total = total_res.scalar_one()

    cat_res = await db.execute(
        select(DexEntry.category, func.count()).group_by(DexEntry.category)
    )
    by_category = {row[0]: row[1] for row in cat_res.all()}

    status_res = await db.execute(
        select(DexEntry.status, func.count()).group_by(DexEntry.status)
    )
    by_status = {row[0]: row[1] for row in status_res.all()}

    avg_res = await db.execute(select(func.coalesce(func.avg(DexEntry.rating), 0.0)))
    average_rating = round(avg_res.scalar_one(), 1)

    return {
        "total": total,
        "byCategory": by_category,
        "byStatus": by_status,
        "averageRating": average_rating,
    }


async def get_dex_entry_by_slug(db: AsyncSession, slug: str) -> DexEntry | None:
    res = await db.execute(select(DexEntry).where(DexEntry.slug == slug))
    return res.scalar_one_or_none()


async def get_dex_entry_by_id(db: AsyncSession, entry_id: str) -> DexEntry | None:
    res = await db.execute(select(DexEntry).where(DexEntry.id == entry_id))
    return res.scalar_one_or_none()


async def create_dex_entry(db: AsyncSession, data: DexEntryCreate) -> DexEntry:
    """创建新的 Dex 条目"""
    # 提取 genre_ids（排除关联字段，避免直接传入模型）
    genre_ids = data.genre_ids

    # 准备基础字段（排除 genre_ids）
    entry_data = data.model_dump(exclude={"genre_ids"})

    # 创建 DexEntry 实例
    entry = DexEntry(**entry_data)

    # 处理多对多关联：绑定标签
    if genre_ids:
        stmt = select(DexGenre).where(DexGenre.id.in_(genre_ids))
        result = await db.execute(stmt)
        genres = result.scalars().all()
        entry.genres = genres  # 设置关联关系

    db.add(entry)
    await db.commit()
    await db.refresh(entry)

    # 重新加载关联数据（确保返回的对象包含 genres）
    stmt = (
        select(DexEntry)
        .options(selectinload(DexEntry.genres))
        .where(DexEntry.id == entry.id)
    )
    result = await db.execute(stmt)
    return result.scalar_one()


async def update_dex_entry(db: AsyncSession, entry: DexEntry, data: DexEntryUpdate) -> DexEntry:
    """更新 Dex 条目"""
    # 获取需更新的字段（仅更新客户端提供的字段）
    update_data = data.model_dump(exclude_unset=True)

    # 单独处理多对多关联字段
    genre_ids = update_data.pop("genre_ids", None)

    # 更新普通字段
    for key, value in update_data.items():
        setattr(entry, key, value)

    # 处理标签关联更新
    if genre_ids is not None:
        # 清空现有关联
        entry.genres.clear()

        # 绑定新标签（如果有）
        if genre_ids:
            stmt = select(DexGenre).where(DexGenre.id.in_(genre_ids))
            result = await db.execute(stmt)
            genres = result.scalars().all()
            entry.genres.extend(genres)

    await db.commit()
    await db.refresh(entry)

    # 重新加载关联数据
    stmt = (
        select(DexEntry)
        .options(selectinload(DexEntry.genres))
        .where(DexEntry.id == entry.id)
    )
    result = await db.execute(stmt)
    return result.scalar_one()


async def delete_dex_entry(db: AsyncSession, entry: DexEntry) -> None:
    await db.delete(entry)
    await db.commit()
