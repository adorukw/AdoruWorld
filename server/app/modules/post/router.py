from collections import defaultdict
from typing import Annotated

from app.common.utils import format_post
from app.core.database import get_db
from app.modules.post_category.schema import PostCategoryResponse
from app.modules.post_tag.schema import PostTagResponse
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .schema import (
    ArchiveItem,
    PostArchiveResponse,
    PostCreate,
    PostResponse,
    PostUpdate,
)

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("", response_model=list[PostResponse])
async def list_posts(
    db: Annotated[AsyncSession, Depends(get_db)],
    published: bool | None = None,
    featured: bool | None = None,
    category: str | None = None,
    tag: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    row = await crud.get_posts(
        db,
        published=published,
        featured=featured,
        category_slug=category,
        tag_slug=tag,
        skip=skip,
        limit=limit,
    )
    return [PostResponse(**format_post(post)) for post in row]


@router.get("/total-posts-count", response_model=int)
async def total_posts_count(db: Annotated[AsyncSession, Depends(get_db)]):
    count = await crud.get_total_posts_count(db)
    return count


@router.get("/total-words", response_model=int)
async def total_words_count(db: Annotated[AsyncSession, Depends(get_db)]):
    count = await crud.get_total_words(db)
    return count


@router.get("/total-views", response_model=int)
async def total_views_count(db: Annotated[AsyncSession, Depends(get_db)]):
    count = await crud.get_total_views(db)
    return count


@router.get("/archives", response_model=list[ArchiveItem])
async def list_archives(db: Annotated[AsyncSession, Depends(get_db)]):
    rows = await crud.get_archive_posts(db)
    grouped: dict[tuple[int, int], list] = defaultdict(list)
    for post in rows:
        created_time = post.created_at
        key = (created_time.year, created_time.month)
        grouped[key].append(
            PostArchiveResponse(
                id=post.id,
                slug=post.slug,
                title=post.title,
                description=post.description,
                cover_image=post.cover_image,
                created_at=post.created_at.isoformat() if post.created_at else "",
                updated_at=post.updated_at.isoformat() if post.updated_at else "",
                published=post.published,
                reading_time=post.reading_time,
                word_count=post.word_count,
                views=post.views,
                featured=post.featured,
                category=PostCategoryResponse.model_validate(post.category)
                if post.category
                else None,
                tags=[PostTagResponse.model_validate(t) for t in post.tags],
            )
        )
    res = []
    for (year, month), items in sorted(grouped.items(), reverse=True):
        res.append(ArchiveItem(year=year, month=month, posts=items))
    return res


@router.get("/slug/{slug}", response_model=PostResponse)
async def get_post_by_slug(slug: str, db: Annotated[AsyncSession, Depends(get_db)]):
    post = await crud.get_post_by_slug(db, slug)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    await crud.increment_views(db, post)
    return PostResponse(**format_post(post))


@router.get("/slug/{slug}/related", response_model=list[PostResponse])
async def get_related_posts(slug: str, db: Annotated[AsyncSession, Depends(get_db)]):
    post = await crud.get_post_by_slug(db, slug)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    related_posts = await crud.get_related_posts(db, post, limit=3)
    return [PostResponse(**format_post(post)) for post in related_posts]


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: str, db: Annotated[AsyncSession, Depends(get_db)]):
    post = await crud.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return PostResponse(**format_post(post))


@router.post("", response_model=PostResponse, status_code=201)
async def create_post(data: PostCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    post = await crud.create_post(db, data)
    return PostResponse(**format_post(post))


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: str, data: PostUpdate, db: Annotated[AsyncSession, Depends(get_db)]
):
    post = await crud.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post = await crud.update_post(db, post, data)
    return PostResponse(**format_post(post))


@router.delete("/{post_id}", status_code=204)
async def delete_post(post_id: str, db: Annotated[AsyncSession, Depends(get_db)]):
    post = await crud.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    await crud.delete_post(db, post)


@router.post("/increment-views/{post_id}", status_code=204)
async def increment_views(post_id: str, db: Annotated[AsyncSession, Depends(get_db)]):
    post = await crud.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    await crud.increment_views(db, post)
