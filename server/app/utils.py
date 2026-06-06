from typing import Any

from app.models import Post as PostModel
from app.schemas import PostCategoryResponse, PostTagResponse


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
        "category": PostCategoryResponse.model_validate(post.category) if post.category else None,
        "tags": [PostTagResponse.model_validate(t) for t in post.tags],
    }
