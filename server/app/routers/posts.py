from datetime import datetime
from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.crud import posts as crud
from app.schemas import PostResponse, PostCreate, PostUpdate, PostListItem, ArchiveItem
from app.utils import format_post

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("", response_model=list[PostListItem])
async def list_posts(
    published: bool | None = None,
    featured: bool | None = None,
    category: str | None = None,
    tag: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    row = await crud.get_posts(db, published=published, featured=featured, category_slug=category, tag_slug=tag, skip=skip, limit=limit)
    return [PostListItem(**format_post(post)) for post in row]


@router.get("/total-posts-count", response_model=int)
async def total_posts_count(db: AsyncSession = Depends(get_db)):
    count = await crud.get_total_posts_count(db)
    return count


@router.get("/total-words", response_model=int)
async def total_words_count(db: AsyncSession = Depends(get_db)):
    count = await crud.get_total_words(db)
    return count


@router.get("/total-views", response_model=int)
async def total_views_count(db: AsyncSession = Depends(get_db)):
    count = await crud.get_total_views(db)
    return count


@router.get("/archives", response_model=list[ArchiveItem])
async def list_archives(db: AsyncSession = Depends(get_db)):
    rows = await crud.get_posts(db, published=True, skip=0, limit=10000)
    grouped: dict[tuple[int, int], list] = defaultdict(list)
    for post in rows:
        data = format_post(post)
        created_time = post.created_at
        key = (created_time.year, created_time.month)
        grouped[key].append(PostListItem(**data))
    res = []
    for (year, month), items in sorted(grouped.items(), reverse=True):
        res.append(ArchiveItem(year=year, month=month, posts=items))
    return res


@router.get("/slug/{slug}", response_model=PostResponse)
async def get_post_by_slug(slug: str, db: AsyncSession = Depends(get_db)):
    post = await crud.get_post_by_slug(db, slug)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    await crud.increment_views(db, post)
    return PostResponse(**format_post(post))


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: str, db: AsyncSession = Depends(get_db)):
    post = await crud.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return PostResponse(**format_post(post))


@router.post("", response_model=PostResponse, status_code=201)
async def create_post(data: PostCreate, db: AsyncSession = Depends(get_db)):
    post = await crud.create_post(db, data)
    return PostResponse(**format_post(post))


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(post_id: str, data: PostUpdate, db: AsyncSession = Depends(get_db)):
    post = await crud.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post = await crud.update_post(db, post, data)
    return PostResponse(**format_post(post))


@router.delete("/{post_id}", status_code=204)
async def delete_post(post_id: str, db: AsyncSession = Depends(get_db)):
    post = await crud.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    await crud.delete_post(db, post)


@router.post("/increment-views/{post_id}", status_code=204)
async def increment_views(post_id: str, db: AsyncSession = Depends(get_db)):
    post = await crud.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    await crud.increment_views(db, post)
