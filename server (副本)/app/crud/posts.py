from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Post, PostCategory, PostTag
from app.schemas import PostCreate, PostUpdate
import uuid
import re


def calculate_reading_time(content: str) -> int:
    """
    计算文章阅读时长（分钟）

    规则：
    - 英文：每分钟 200-250 个单词
    - 中文：每分钟 300-400 个字符
    - 代码块：不计阅读时间
    - 图片：每张图片额外增加 12 秒

    返回：阅读时长（分钟，向上取整）
    """
    if not content:
        return 0

    # 1. 移除 Markdown 代码块
    content_without_code = re.sub(r'```[\s\S]*?```', '', content)
    content_without_code = re.sub(r'`[^`]+`', '', content_without_code)

    # 2. 统计图片数量（Markdown 图片语法 ![alt](url)）
    image_count = len(re.findall(r'!\[.*?\]\(.*?\)', content))

    # 3. 统计纯文本字符数（移除 Markdown 标记）
    # 移除标题标记 #
    text = re.sub(r'^#+\s*', '', content_without_code, flags=re.MULTILINE)
    # 移除粗体、斜体标记
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'__(.*?)__', r'\1', text)
    text = re.sub(r'_(.*?)_', r'\1', text)
    # 移除链接标记
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    # 移除列表标记
    text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)
    # 移除引用标记
    text = re.sub(r'^\s*>\s+', '', text, flags=re.MULTILINE)

    # 4. 计算字符数（中文字符算 1 个，英文字符也算 1 个）
    char_count = len(text.strip())

    # 5. 计算阅读时间
    # 中文阅读速度：约 400 字符/分钟
    # 英文阅读速度：约 200 单词/分钟
    # 我们取平均值：300 字符/分钟
    base_reading_time = char_count / 300

    # 6. 图片额外时间：每张图片增加 0.2 分钟（12秒）
    image_time = image_count * 0.2

    total_time = base_reading_time + image_time

    # 7. 向上取整，最少 1 分钟
    return max(1, int(total_time + 0.99))


async def get_posts(
    db: AsyncSession,
    published: bool | None = None,
    featured: bool | None = None,
    category_slug: str | None = None,
    tag_slug: str | None = None,
    skip: int = 0,
    limit: int = 20
) -> list[Post]:
    stmt = select(Post).options(
        selectinload(Post.category),
        selectinload(Post.tags)
    )
    if published is not None:
        stmt = stmt.where(Post.published == published)
    if featured is not None:
        stmt = stmt.where(Post.featured == featured)
    if category_slug:
        stmt = stmt.join(Post.category).where(
            PostCategory.slug == category_slug)
    if tag_slug:
        stmt = stmt.join(Post.tags).where(PostTag.slug == tag_slug)
    stmt = stmt.order_by(Post.created_at.desc()).offset(skip).limit(limit)
    res = await db.execute(stmt)
    return list(res.scalars().all())


async def get_post_by_slug(db: AsyncSession, slug: str) -> Post | None:
    stmt = select(Post).options(
        selectinload(Post.category),
        selectinload(Post.tags)
    ).where(Post.slug == slug)
    res = await db.execute(stmt)
    return res.scalar_one_or_none()


async def get_post_by_id(db: AsyncSession, post_id: str) -> Post | None:
    stmt = select(Post).options(
        selectinload(Post.category),
        selectinload(Post.tags)
    ).where(Post.id == post_id)
    res = await db.execute(stmt)
    return res.scalar_one_or_none()


async def create_post(db: AsyncSession, data: PostCreate) -> Post:
    """创建新文章"""
    # 提取标签 ID，从数据中排除，避免直接传入 Post 构造函数
    tag_ids = data.tag_ids

    # 准备文章数据（不包含标签）
    post_data = data.model_dump(exclude={"tag_ids"})

    if 'content' in post_data and post_data['content']:
        reading_time = calculate_reading_time(post_data['content'])
        post_data['reading_time'] = reading_time

        # 同时计算字数（字符数）
        word_count = len(post_data['content'].strip())
        post_data['word_count'] = word_count

    # 创建文章实例
    post = Post(**post_data)

    # 处理标签关联
    if tag_ids:
        # 查询存在的标签
        stmt = select(PostTag).where(PostTag.id.in_(tag_ids))
        result = await db.execute(stmt)
        tags = result.scalars().all()
        post.tags = tags  # 设置关联关系

    db.add(post)
    await db.commit()
    await db.refresh(post)

    # 重新加载关联数据以确保返回完整对象
    stmt = (
        select(Post)
        .options(selectinload(Post.category), selectinload(Post.tags))
        .where(Post.id == post.id)
    )
    result = await db.execute(stmt)
    return result.scalar_one()


async def update_post(db: AsyncSession, post: Post, data: PostUpdate) -> Post:
    """更新文章"""
    # 获取要更新的字段（排除未设置的字段）
    update_data = data.model_dump(exclude_unset=True)

    # 单独处理标签
    tag_ids = update_data.pop("tag_ids", None)

    if "content" in update_data and update_data["content"]:
        reading_time = calculate_reading_time(update_data["content"])
        update_data["reading_time"] = reading_time

        # 同时更新字数
        word_count = len(update_data["content"].strip())
        update_data["word_count"] = word_count

    # 更新普通字段
    for key, value in update_data.items():
        setattr(post, key, value)

    # 更新标签关联
    if tag_ids is not None:
        # 清除现有标签
        post.tags.clear()

        # 如果有新的标签 ID，则添加
        if tag_ids:
            stmt = select(PostTag).where(PostTag.id.in_(tag_ids))
            result = await db.execute(stmt)
            tags = result.scalars().all()
            post.tags.extend(tags)

    await db.commit()
    await db.refresh(post)

    # 重新加载关联数据
    stmt = (
        select(Post)
        .options(selectinload(Post.category), selectinload(Post.tags))
        .where(Post.id == post.id)
    )
    result = await db.execute(stmt)
    return result.scalar_one()


async def delete_post(db: AsyncSession, post: Post) -> None:
    await db.delete(post)
    await db.commit()


async def increment_views(db: AsyncSession, post: Post) -> Post:
    post.views += 1
    await db.commit()
    await db.refresh(post)
    return post


async def get_total_posts_count(db: AsyncSession, published_only: bool = True) -> int:
    stmt = select(func.count()).select_from(Post)
    if published_only:
        stmt = stmt.where(Post.published == True)
    res = await db.execute(stmt)
    return res.scalar_one_or_none()


async def get_total_words(db: AsyncSession) -> int:
    stmt = select(func.coalesce(func.sum(Post.word_count),
                  0)).where(Post.published == True)
    res = await db.execute(stmt)
    return res.scalar_one()


async def get_total_views(db: AsyncSession) -> int:
    stmt = select(func.coalesce(func.sum(Post.views),
                  0)).where(Post.published == True)
    res = await db.execute(stmt)
    return res.scalar_one()
