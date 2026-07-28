import os
from contextlib import asynccontextmanager

from app.core.config import API_PREFIX, DESCRIPTION, PROJECT_NAME, VERSION
from app.core.database import init_db
from app.modules import (
    dex_genres_router,
    dexs_router,
    media_tags_router,
    medias_router,
    post_categories_router,
    post_tags_router,
    posts_router,
    search_router,
    system_router,
)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title=PROJECT_NAME, version=VERSION, description=DESCRIPTION, lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts_router, prefix=API_PREFIX)
app.include_router(post_categories_router, prefix=API_PREFIX)
app.include_router(post_tags_router, prefix=API_PREFIX)
app.include_router(dexs_router, prefix=API_PREFIX)
app.include_router(dex_genres_router, prefix=API_PREFIX)
app.include_router(system_router, prefix=API_PREFIX)
app.include_router(medias_router, prefix=API_PREFIX)
app.include_router(media_tags_router, prefix=API_PREFIX)
app.include_router(search_router, prefix=API_PREFIX)

if not os.path.exists("uploads"):
    os.makedirs("uploads")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/")
async def root():
    return {"name": PROJECT_NAME, "version": VERSION}
