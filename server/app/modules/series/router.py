from typing import Annotated

from app.core.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from app.modules.auth.dependency import require_role
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .schema import (
    SeriesCreate,
    SeriesPostResponse,
    SeriesResponse,
    SeriesUpdate,
)

router = APIRouter(prefix="/series", tags=["series"])


def _to_response(series, count: int) -> SeriesResponse:
    resp = SeriesResponse.model_validate(series)
    resp.count = count
    return resp


@router.get("", response_model=list[SeriesResponse])
async def list_series(db: Annotated[AsyncSession, Depends(get_db)]):
    rows = await crud.get_series_list(db)
    res = []
    for s in rows:
        count = await crud.get_series_count(db, s.id)
        res.append(_to_response(s, count))
    return res


@router.get("/slug/{slug}", response_model=SeriesResponse)
async def get_series_by_slug(slug: str, db: Annotated[AsyncSession, Depends(get_db)]):
    series = await crud.get_series_by_slug(db, slug)
    if not series:
        raise HTTPException(status_code=404, detail="Series not found")
    count = await crud.get_series_count(db, series.id)
    return _to_response(series, count)


@router.get("/{series_id}", response_model=SeriesResponse)
async def get_series(series_id: str, db: Annotated[AsyncSession, Depends(get_db)]):
    series = await crud.get_series_by_id(db, series_id)
    if not series:
        raise HTTPException(status_code=404, detail="Series not found")
    count = await crud.get_series_count(db, series.id)
    return _to_response(series, count)


@router.get("/{series_id}/posts", response_model=list[SeriesPostResponse])
async def get_series_posts(
    series_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    published: bool | None = None,
):
    series = await crud.get_series_by_id(db, series_id)
    if not series:
        raise HTTPException(status_code=404, detail="Series not found")
    posts = await crud.get_series_posts(
        db, series_id, published_only=True if published else False
    )
    return [SeriesPostResponse.model_validate(p) for p in posts]


@router.post("", response_model=SeriesResponse, status_code=201, dependencies=[Depends(require_role('admin', 'editor'))])
async def create_series(data: SeriesCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    series = await crud.create_series(db, data)
    return _to_response(series, 0)


@router.put("/{series_id}", response_model=SeriesResponse, dependencies=[Depends(require_role('admin', 'editor'))])
async def update_series(
    series_id: str, data: SeriesUpdate, db: Annotated[AsyncSession, Depends(get_db)]
):
    series = await crud.get_series_by_id(db, series_id)
    if not series:
        raise HTTPException(status_code=404, detail="Series not found")
    series = await crud.update_series(db, series, data)
    count = await crud.get_series_count(db, series.id)
    return _to_response(series, count)


@router.delete("/{series_id}", status_code=204, dependencies=[Depends(require_role('admin', 'editor'))])
async def delete_series(series_id: str, db: Annotated[AsyncSession, Depends(get_db)]):
    series = await crud.get_series_by_id(db, series_id)
    if not series:
        raise HTTPException(status_code=404, detail="Series not found")
    await crud.delete_series(db, series)
