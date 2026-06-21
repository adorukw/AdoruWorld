from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.crud import post_categories as crud
from app.schemas import PostCategoryResponse, PostCategoryCreate, PostCategoryUpdate

router = APIRouter(prefix="/post_categories", tags=["post_categories"])


@router.get("", response_model=list[PostCategoryResponse])
async def list_categories(db: AsyncSession = Depends(get_db)):
    rows = await crud.get_categories(db)
    res = []
    for c in rows:
        count = await crud.get_category_count(db, c.id)
        res.append(PostCategoryResponse(
            id=c.id, name=c.name, slug=c.slug, description=c.description,
            icon=c.icon, color=c.color, count=count
        ))
    return res


@router.get("/slug/{slug}", response_model=PostCategoryResponse)
async def get_category_by_slug(slug: str, db: AsyncSession = Depends(get_db)):
    category = await crud.get_category_by_slug(db, slug)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    count = await crud.get_category_count(db, category.id)
    return PostCategoryResponse(
        id=category.id, name=category.name, slug=category.slug,
        description=category.description, icon=category.icon,
        color=category.color, count=count
    )


@router.get("/{category_id}", response_model=PostCategoryResponse)
async def get_category_by_id(category_id: str, db: AsyncSession = Depends(get_db)):
    category = await crud.get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    count = await crud.get_category_count(db, category.id)
    return PostCategoryResponse(
        id=category.id, name=category.name, slug=category.slug,
        description=category.description, icon=category.icon, color=category.color, count=count
    )


@router.post("", response_model=PostCategoryResponse, status_code=201)
async def create_category(data: PostCategoryCreate, db: AsyncSession = Depends(get_db)):
    category = await crud.create_category(db, data)
    return PostCategoryResponse(
        id=category.id, name=category.name, slug=category.slug,
        description=category.description, icon=category.icon, color=category.color, count=0
    )


@router.put("/{category_id}", response_model=PostCategoryResponse)
async def update_category(category_id: str, data: PostCategoryUpdate, db: AsyncSession = Depends(get_db)):
    category = await crud.get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category = await crud.update_category(db, category, data)
    count = await crud.get_category_count(db, category.id)
    return PostCategoryResponse(
        id=category.id, name=category.name, slug=category.slug,
        description=category.description, icon=category.icon, color=category.color, count=count
    )


@router.delete("/{category_id}", status_code=204)
async def delete_category(category_id: str, db: AsyncSession = Depends(get_db)):
    category = await crud.get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    await crud.delete_category(db, category)
