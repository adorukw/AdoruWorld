from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import PostTag, post_to_post_tags
from app.schemas import PostTagCreate, PostTagUpdate


async def get_tags(db: AsyncSession) -> list[PostTag]:
    res = await db.execute(select(PostTag))
    return list(res.scalars().all())


async def get_tag_by_slug(db: AsyncSession, slug: str) -> PostTag | None:
    res = await db.execute(select(PostTag).where(PostTag.slug == slug))
    return res.scalar_one_or_none()


async def get_tag_by_id(db: AsyncSession, tag_id: str) -> PostTag | None:
    res = await db.execute(select(PostTag).where(PostTag.id == tag_id))
    return res.scalar_one_or_none()


async def create_tag(db: AsyncSession, data: PostTagCreate) -> PostTag:
    tag = PostTag(**data.model_dump())
    db.add(tag)
    await db.commit()
    await db.refresh(tag)
    return tag


async def update_tag(db: AsyncSession, tag: PostTag, data: PostTagUpdate) -> PostTag:
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(tag, key, value)
    await db.commit()
    await db.refresh(tag)
    return tag


async def delete_tag(db: AsyncSession, tag: PostTag) -> None:
    await db.delete(tag)
    await db.commit()


async def get_tag_count(db: AsyncSession, tag_id: str) -> int:
    stmt = select(func.count()).select_from(
        post_to_post_tags).where(post_to_post_tags.c.post_tag_id == tag_id)
    res = await db.execute(stmt)
    return res.scalar_one() or 0
