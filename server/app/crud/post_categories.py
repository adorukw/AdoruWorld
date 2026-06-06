from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Post, PostCategory
from app.schemas import PostCategoryCreate, PostCategoryUpdate


async def get_categories(db: AsyncSession) -> list[PostCategory]:
    res = await db.execute(select(PostCategory))
    return list(res.scalars().all())


async def get_category_by_slug(db: AsyncSession, slug: str) -> PostCategory | None:
    res = await db.execute(select(PostCategory).where(PostCategory.slug == slug))
    return res.scalar_one_or_none()


async def get_category_by_id(db: AsyncSession, id: str) -> PostCategory | None:
    res = await db.execute(select(PostCategory).where(PostCategory.id == id))
    return res.scalar_one_or_none()


async def create_category(db: AsyncSession, data: PostCategoryCreate) -> PostCategory:
    category = PostCategory(**data.model_dump())
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


async def update_category(db: AsyncSession, category: PostCategory, data: PostCategoryUpdate) -> PostCategory:
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(category, key, value)
    await db.commit()
    await db.refresh(category)
    return category


async def delete_category(db: AsyncSession, category: PostCategory) -> None:
    await db.delete(category)
    await db.commit()


async def get_category_count(db: AsyncSession, category_id: str) -> int:
    stmt = select(func.count(Post.id)).where(Post.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar() or 0
