from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import MediaTag, media_to_media_tags
from app.schemas import MediaTagCreate, MediaTagUpdate


async def get_tags(db: AsyncSession) -> list[MediaTag]:
    res = await db.execute(select(MediaTag))
    return list(res.scalars().all())


async def get_tag_by_slug(db: AsyncSession, slug: str) -> MediaTag | None:
    res = await db.execute(select(MediaTag).where(MediaTag.slug == slug))
    return res.scalar_one_or_none()


async def get_tag_by_id(db: AsyncSession, id: str) -> MediaTag | None:
    res = await db.execute(select(MediaTag).where(MediaTag.id == id))
    return res.scalar_one_or_none()


async def create_tag(db: AsyncSession, data: MediaTagCreate) -> MediaTag:
    tag = MediaTag(**data.model_dump())
    db.add(tag)
    await db.commit()
    await db.refresh(tag)
    return tag


async def update_tag(db: AsyncSession, tag: MediaTag, data: MediaTagUpdate) -> MediaTag:
    update_tag = data.model_dump(exclude_unset=True)
    for key, value in update_tag.items():
        setattr(tag, key, value)
    await db.commit()
    await db.refresh(tag)
    return tag


async def delete_tag(db: AsyncSession, tag: MediaTag) -> None:
    await db.delete(tag)
    await db.commit()
