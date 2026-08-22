from typing import Any

from app.modules.post.model import Post as PostModel
from app.modules.post.schema import PostCategoryResponse, PostTagResponse
from app.modules.series.schema import SeriesResponse


def format_post(post: PostModel) -> dict[str, Any]:
    return {
        "id": post.id,
        "slug": post.slug,
        "title": post.title,
        "description": post.description,
        "content": post.content,
        "cover_image": post.cover_image,
        "created_at": post.created_at.isoformat() if post.created_at else "",
        "updated_at": post.updated_at.isoformat() if post.updated_at else "",
        "published": post.published,
        "reading_time": post.reading_time,
        "word_count": post.word_count,
        "views": post.views,
        "featured": post.featured,
        "category": PostCategoryResponse.model_validate(post.category)
        if post.category
        else None,
        "tags": [PostTagResponse.model_validate(t) for t in post.tags],
        "series": SeriesResponse.model_validate(post.series) if post.series else None,
        "series_order": post.series_order,
    }
