import os
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Media, MediaTag
from app.schemas import MediaCreate, MediaUpdate


async def get_media(
        db: AsyncSession,
        media_type: str | None = None,
        tag_slug: str | None = None,
        skip: int = 0,
        limit: int = 100
) -> list[Media]:
    stmt = select(Media).options(selectinload(Media.tags))

    if media_type:
        stmt = stmt.where(Media.media_type == media_type)
    if tag_slug:
        stmt = stmt.join(Media.tags).where(MediaTag.slug == tag_slug)
    stmt = stmt.order_by(Media.uploaded_at.desc()).offset(skip).limit(limit)
    res = await db.execute(stmt)
    return list(res.scalars().all())


async def get_media_by_slug(db: AsyncSession, slug: str) -> Media | None:
    stmt = select(Media).options(selectinload(
        Media.tags)).where(Media.slug == slug)
    res = await db.execute(stmt)
    return res.scalar_one_or_none()


async def get_media_by_id(db: AsyncSession, media_id: str) -> Media | None:
    stmt = select(Media).options(selectinload(
        Media.tags)).where(Media.id == media_id)
    res = await db.execute(stmt)
    return res.scalar_one_or_none()


async def create_media(db: AsyncSession, data: MediaCreate) -> Media:
    tag_ids = data.tag_ids

    media_data = data.model_dump(exclude={"tag_ids"})

    ext = os.path.splitext(media_data["file_path"])[1].lower()
    media_data["extension"] = ext

    media = Media(**media_data)

    if tag_ids:
        stmt = select(MediaTag).where(MediaTag.id.in_(tag_ids))
        res = await db.execute(stmt)
        tags = res.scalars().all()
        media.tags = tags

    db.add(media)
    await db.commit()
    await db.refresh(media)

    stmt = select(Media).options(selectinload(
        Media.tags)).where(Media.id == media.id)
    res = await db.execute(stmt)
    return res.scalar_one()


async def update_media(db: AsyncSession, media: Media, data: MediaUpdate) -> Media:
    update_data = data.model_dump(exclude_unset=True)

    tag_ids = update_data.pop("tag_ids", None)

    for key, value in update_data.items():
        setattr(media, key, value)

    if tag_ids is not None:
        media.tags.clear()
        if tag_ids:
            stmt = select(MediaTag).where(MediaTag.id.in_(tag_ids))
            result = await db.execute(stmt)
            tags = result.scalars().all()
            media.tags.extend(tags)

    await db.commit()
    await db.refresh(media)

    stmt = select(Media).options(selectinload(
        Media.tags)).where(Media.id == media.id)
    result = await db.execute(stmt)
    return result.scalar_one()


async def delete_media(db: AsyncSession, media: Media) -> None:
    await db.delete(media)
    await db.commit()
