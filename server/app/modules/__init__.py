# routers
from app.modules.post.router import router as posts_router
from app.modules.post_category.router import router as post_categories_router
from app.modules.post_tag.router import router as post_tags_router
from app.modules.dex.router import router as dexs_router
from app.modules.dex_genre.router import router as dex_genres_router
from app.modules.system.router import router as system_router
from app.modules.media.router import router as medias_router
from app.modules.media_tag.router import router as media_tags_router

# models
from app.modules.post.model import Post, post_to_post_tags
from app.modules.post_tag.model import PostTag
from app.modules.post_category.model import PostCategory
from app.modules.dex.model import Dex, dex_to_dex_genres
from app.modules.dex_genre.model import DexGenre
from app.modules.media.model import Media, media_to_media_tags
from app.modules.media_tag.model import MediaTag

__all__ = [
    # routers
    "posts_router", "post_categories_router", "post_tags_router",
    "dexs_router", "dex_genres_router", "system_router",
    "medias_router", "media_tags_router",
    # models
    "Post", "PostTag", "PostCategory", "post_to_post_tags",
    "Dex", "DexGenre", "dex_to_dex_genres",
    "Media", "media_to_media_tags", "MediaTag",
]
