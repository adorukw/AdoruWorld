from app.routers.posts import router as posts_router
from app.routers.post_categories import router as post_categories_router
from app.routers.post_tags import router as post_tags_router
from app.routers.dexs import router as dexs_router
from app.routers.dex_genres import router as dex_genres_router
from app.routers.system import router as system_router
from app.routers.medias import router as medias_router
from app.routers.media_tags import router as media_tags_router

__all__ = [
    "posts_router",
    "post_categories_router",
    "post_tags_router",
    "dexs_router",
    "dex_genres_router",
    "system_router",
    "medias_router",
    "media_tags_router",
]
