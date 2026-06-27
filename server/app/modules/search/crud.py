"""
GlobalSearch CRUD — 跨 Post / Dex / Media 的关键词搜索。

核心策略：
  1. 将查询字符串按空格、逗号拆分成多个关键词（AND 逻辑）。
  2. 对每个关键词，用 OR 比对模型的文本字段 + 关联分类/标签的名称。
  3. 多关键词之间用 AND 联结 —— 结果必须同时匹配所有关键词。
  4. 通过 outerjoin 搜索关联表的字段（分类名、标签名、题材名），
     用 distinct() 去重，避免多对多 JOIN 产生的重复行。
  5. 各实体搜索完后统一按时间降序排序（Dex 无时间字段，按标题排在最末）。
"""

import re
from datetime import datetime

from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.post.model import Post
from app.modules.post_category.model import PostCategory
from app.modules.post_tag.model import PostTag
from app.modules.dex.model import Dex
from app.modules.dex_genre.model import DexGenre
from app.modules.media.model import Media
from app.modules.media_tag.model import MediaTag

# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------


def _split_keywords(q: str) -> list[str]:
    """将查询串拆成多个关键词，过滤空串。"""
    return [kw.strip() for kw in re.split(r"[\s,，]+", q) if kw.strip()]


def _text_contains(text: str | None, keyword: str) -> bool:
    """忽略大小写检查一段文本是否包含某个关键词。"""
    if not text:
        return False
    return keyword.lower() in text.lower()


def _any_keyword_in(text: str | None, keywords: list[str]) -> bool:
    """一段文本是否包含任意一个关键词。"""
    return any(_text_contains(text, kw) for kw in keywords)


def _get_matched_fields(entity, etype: str, keywords: list[str]) -> list[str]:
    """
    遍历实体的可搜索字段，返回命中关键词的字段名列表。
    前端拿到后可用来做高亮。
    """
    if etype == "post":
        candidates = [
            ("title", entity.title),
            ("description", entity.description or ""),
            ("content", entity.content),
            ("category", entity.category.name if entity.category else ""),
            ("tags", " ".join(t.name for t in entity.tags)),
        ]
    elif etype == "dex":
        candidates = [
            ("title", entity.title),
            ("original_title", entity.original_title or ""),
            ("summary", entity.summary or ""),
            ("comment", entity.comment or ""),
            ("creator", entity.creator or ""),
            ("genres", " ".join(g.name for g in entity.genres)),
        ]
    elif etype == "media":
        candidates = [
            ("title", entity.title),
            ("file_path", entity.file_path),
            ("tags", " ".join(t.name for t in entity.tags)),
        ]
    else:
        candidates = [("title", entity.title)]

    return [name for name, val in candidates if _any_keyword_in(val, keywords)]


def _dt_str(dt: datetime | None) -> str | None:
    return dt.isoformat() if dt else None


def _pick_description(entity, etype: str) -> str | None:
    """统一提取一个适合展示在搜索卡片上的简短描述。"""
    if etype == "post":
        return entity.description or (entity.content[:200] if entity.content else None)
    if etype == "dex":
        return entity.summary or entity.comment
    return None


def _pick_cover_image(entity, etype: str) -> str | None:
    """统一提取封面图 URL。"""
    if etype in ("post", "dex"):
        return entity.cover_image
    if etype == "media" and entity.media_type == "image":
        return entity.file_path
    return None


def _entity_to_dict(entity, etype: str) -> dict:
    """
    将 SQLAlchemy 实体转成纯 dict（不依赖 schema 模型以避免循环导入）。
    只暴露前端渲染和导航所需的字段。
    """
    base = {"id": entity.id, "slug": entity.slug, "title": entity.title}

    if etype == "post":
        base.update(
            description=entity.description,
            content=entity.content,
            cover_image=entity.cover_image,
            created_at=_dt_str(entity.created_at),
            updated_at=_dt_str(entity.updated_at),
            published=entity.published,
            featured=entity.featured,
            reading_time=entity.reading_time,
            word_count=entity.word_count,
            views=entity.views,
            category=(
                {"id": entity.category.id, "name": entity.category.name,
                 "slug": entity.category.slug}
                if entity.category
                else None
            ),
            tags=[
                {"id": t.id, "name": t.name, "slug": t.slug}
                for t in entity.tags
            ],
        )
    elif etype == "dex":
        base.update(
            original_title=entity.original_title,
            cover_image=entity.cover_image,
            category=entity.category,
            status=entity.status,
            rating=entity.rating,
            summary=entity.summary,
            comment=entity.comment,
            creator=entity.creator,
            year=entity.year,
            genres=[
                {"id": g.id, "name": g.name, "slug": g.slug}
                for g in entity.genres
            ],
        )
    elif etype == "media":
        base.update(
            file_path=entity.file_path,
            file_size=entity.file_size,
            media_type=entity.media_type,
            mime_type=entity.mime_type,
            extension=entity.extension,
            meta_data=entity.meta_data,
            uploaded_at=_dt_str(entity.uploaded_at),
            tags=[
                {"id": t.id, "name": t.name, "slug": t.slug}
                for t in entity.tags
            ],
        )

    return base

# ---------------------------------------------------------------------------
# 各实体搜索
# ---------------------------------------------------------------------------


async def _search_posts(
    db: AsyncSession,
    keywords: list[str],
    skip: int,
    limit: int,
) -> tuple[list[Post], int]:
    """搜索 Post：匹配 title / description / content / 分类名 / 标签名。"""
    conditions = [
        or_(
            Post.title.ilike(f"%{kw}%"),
            Post.description.ilike(f"%{kw}%"),
            Post.content.ilike(f"%{kw}%"),
            PostCategory.name.ilike(f"%{kw}%"),
            PostTag.name.ilike(f"%{kw}%"),
        )
        for kw in keywords
    ]

    # 用 COUNT(DISTINCT id) 取总数
    id_subq = (
        select(Post.id)
        .outerjoin(Post.tags)
        .outerjoin(Post.category)
        .where(and_(*conditions))
        .where(Post.published == True)
        .distinct()
        .subquery()
    )
    count_result = await db.execute(select(func.count()).select_from(id_subq))
    total = count_result.scalar_one()

    # 分页查询：distinct → order_by → offset / limit
    stmt = (
        select(Post)
        .options(selectinload(Post.category), selectinload(Post.tags))
        .outerjoin(Post.tags)
        .outerjoin(Post.category)
        .where(and_(*conditions))
        .where(Post.published == True)
        .distinct()
        .order_by(Post.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    posts = list(result.scalars().all())

    # 由于上面用 outerjoin + selectinload 混用，selectinload 仍然会独立发额外 SQL，
    # 所以关联数据是完整的，不需要二次查询。
    return posts, total


async def _search_dexs(
    db: AsyncSession,
    keywords: list[str],
    skip: int,
    limit: int,
) -> tuple[list[Dex], int]:
    """
    搜索 Dex：匹配 title / original_title / summary / comment / creator / 题材名。
    """
    conditions = [
        or_(
            Dex.title.ilike(f"%{kw}%"),
            Dex.original_title.ilike(f"%{kw}%"),
            Dex.summary.ilike(f"%{kw}%"),
            Dex.comment.ilike(f"%{kw}%"),
            Dex.creator.ilike(f"%{kw}%"),
            DexGenre.name.ilike(f"%{kw}%"),
        )
        for kw in keywords
    ]

    id_subq = (
        select(Dex.id)
        .outerjoin(Dex.genres)
        .where(and_(*conditions))
        .distinct()
        .subquery()
    )
    total = (await db.execute(select(func.count()).select_from(id_subq))).scalar_one()

    stmt = (
        select(Dex)
        .options(selectinload(Dex.genres))
        .outerjoin(Dex.genres)
        .where(and_(*conditions))
        .distinct()
        .order_by(Dex.title)
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return list(result.scalars().all()), total


async def _search_medias(
    db: AsyncSession,
    keywords: list[str],
    skip: int,
    limit: int,
) -> tuple[list[Media], int]:
    """
    搜索 Media：匹配 title / file_path / 标签名。
    (meta_data 为 JSON 列，不太适合用 like 全文搜，暂不纳入)
    """
    conditions = [
        or_(
            Media.title.ilike(f"%{kw}%"),
            Media.file_path.ilike(f"%{kw}%"),
            MediaTag.name.ilike(f"%{kw}%"),
        )
        for kw in keywords
    ]

    id_subq = (
        select(Media.id)
        .outerjoin(Media.tags)
        .where(and_(*conditions))
        .distinct()
        .subquery()
    )
    total = (await db.execute(select(func.count()).select_from(id_subq))).scalar_one()

    stmt = (
        select(Media)
        .options(selectinload(Media.tags))
        .outerjoin(Media.tags)
        .where(and_(*conditions))
        .distinct()
        .order_by(Media.uploaded_at.desc())
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return list(result.scalars().all()), total

# ---------------------------------------------------------------------------
# 统一搜索入口
# ---------------------------------------------------------------------------


async def search_all(
    db: AsyncSession,
    q: str,
    entity_type: str | None = None,
    skip: int = 0,
    limit: int = 20,
) -> tuple[list[dict], int]:
    """
    全站关键词搜索。

    参数
    ----
    q : str
        查询字符串。空格或逗号分隔多个关键词（AND 语义）。
    entity_type : str | None
        可选筛 "post" / "dex" / "media"，None 表示全部。
    skip, limit : int
        分页。

    返回
    ----
    (items, total)
        items : list[dict] — 每项结构见 schema.SearchResultItem。
        total : int — 匹配总数（分页前）。
    """
    keywords = _split_keywords(q)
    if not keywords:
        return [], 0

    # 收集 (sort_timestamp, type, entity) 三元组
    raw: list[tuple[float, str, object]] = []

    if entity_type in (None, "post"):
        posts, _ = await _search_posts(db, keywords, 0, 1000)
        for p in posts:
            ts = p.created_at.timestamp() if p.created_at else 0
            raw.append((ts, "post", p))

    if entity_type in (None, "dex"):
        dexs, _ = await _search_dexs(db, keywords, 0, 1000)
        for d in dexs:
            raw.append((-1.0, "dex", d))  # 负值确保排在时序实体之后

    if entity_type in (None, "media"):
        medias, _ = await _search_medias(db, keywords, 0, 1000)
        for m in medias:
            ts = m.uploaded_at.timestamp() if m.uploaded_at else 0
            raw.append((ts, "media", m))

    # 排序：时间降序；同时部分按 title 升序作二次排序
    raw.sort(key=lambda x: (-x[0], x[2].title or ""))

    total = len(raw)
    page = raw[skip: skip + limit]

    items = [_build_item(it, keywords) for it in page]
    return items, total


def _build_item(item: tuple, keywords: list[str]) -> dict:
    """将 (ts, etype, entity) 转为 SearchResultItem 格式的 dict。"""
    _, etype, entity = item
    return {
        "id": entity.id,
        "type": etype,
        "title": entity.title,
        "slug": entity.slug,
        "description": _pick_description(entity, etype),
        "cover_image": _pick_cover_image(entity, etype),
        "created_at": _dt_str(
            entity.created_at
            if etype == "post"
            else entity.uploaded_at
            if etype == "media"
            else None
        ),
        "matched_fields": _get_matched_fields(entity, etype, keywords),
        "entity_data": _entity_to_dict(entity, etype),
    }
