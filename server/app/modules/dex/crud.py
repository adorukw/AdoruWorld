from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .model import Dex
from .model import DexGenre
from .schema import DexCreate, DexUpdate


async def get_dex(
        db: AsyncSession,
        category: str | None = None,
        status: str | None = None,
        skip: int = 0,
        limit: int = 20
) -> list[Dex]:
    stmt = select(Dex)
    if category:
        stmt = stmt.where(Dex.category == category)
    if status:
        stmt = stmt.where(Dex.status == status)
    stmt = stmt.order_by(Dex.title).offset(skip).limit(limit)
    res = await db.execute(stmt)
    return list(res.scalars().all())


async def get_dex_stats(db: AsyncSession) -> dict:
    total_res = await db.execute(select(func.count()).select_from(Dex))
    total = total_res.scalar_one()

    cat_res = await db.execute(
        select(Dex.category, func.count()).group_by(Dex.category)
    )
    by_category = {row[0]: row[1] for row in cat_res.all()}

    status_res = await db.execute(
        select(Dex.status, func.count()).group_by(Dex.status)
    )
    by_status = {row[0]: row[1] for row in status_res.all()}

    avg_res = await db.execute(select(func.coalesce(func.avg(Dex.rating), 0.0)))
    average_rating = round(avg_res.scalar_one(), 1)

    return {
        "total": total,
        "byCategory": by_category,
        "byStatus": by_status,
        "averageRating": average_rating,
    }


async def get_dex_by_slug(db: AsyncSession, slug: str) -> Dex | None:
    res = await db.execute(select(Dex).where(Dex.slug == slug))
    return res.scalar_one_or_none()


async def get_dex_by_id(db: AsyncSession, entry_id: str) -> Dex | None:
    res = await db.execute(select(Dex).where(Dex.id == entry_id))
    return res.scalar_one_or_none()


async def create_dex(db: AsyncSession, data: DexCreate) -> Dex:
    """创建新的 Dex 条目"""
    # 提取 genre_ids（排除关联字段，避免直接传入模型）
    genre_ids = data.genre_ids

    # 准备基础字段（排除 genre_ids）
    entry_data = data.model_dump(exclude={"genre_ids"})

    # 创建 DexEntry 实例
    entry = Dex(**entry_data)

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
        select(Dex)
        .options(selectinload(Dex.genres))
        .where(Dex.id == entry.id)
    )
    result = await db.execute(stmt)
    return result.scalar_one()


async def update_dex(db: AsyncSession, entry: Dex, data: DexUpdate) -> Dex:
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
        select(Dex)
        .options(selectinload(Dex.genres))
        .where(Dex.id == entry.id)
    )
    result = await db.execute(stmt)
    return result.scalar_one()


async def delete_dex(db: AsyncSession, entry: Dex) -> None:
    await db.delete(entry)
    await db.commit()
