import asyncio
import os
import random
import re
import uuid
from datetime import datetime, timedelta, timezone

from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session, init_db
from app.modules import (
    PostCategory, PostTag, Post, post_to_post_tags,
    Dex, DexGenre, dex_to_dex_genres,
    Media, MediaTag, media_to_media_tags
)

fake = Faker('zh_CN')

# ============================================================
# 固定种子：分类、标签、题材（数量少且语义明确，手动定义）
# ============================================================

CATEGORIES = [
    {"name": "技术笔记", "slug": "tech", "icon": "💻", "color": "#3C5AA6"},
    {"name": "生活随笔", "slug": "life", "icon": "🌸", "color": "#FF7300"},
    {"name": "开发日志", "slug": "projects", "icon": "🚀", "color": "#FF0000"},
    {"name": "读书笔记", "slug": "reading", "icon": "📚", "color": "#7B5BA6"},
    {"name": "游戏人生", "slug": "gaming", "icon": "🎮", "color": "#FFDE00"},
    {"name": "创意思考", "slug": "creative", "icon": "✨", "color": "#9CBB0F"},
]

TAGS = [
    # 语言/框架
    {"name": "Vue", "slug": "vue", "color": "#42b883"},
    {"name": "React", "slug": "react", "color": "#61dafb"},
    {"name": "TypeScript", "slug": "typescript", "color": "#3178c6"},
    {"name": "Node.js", "slug": "nodejs", "color": "#68a063"},
    {"name": "Python", "slug": "python", "color": "#3776AB"},
    {"name": "Rust", "slug": "rust", "color": "#DEA584"},
    {"name": "Go", "slug": "go", "color": "#00ADD8"},
    # 领域
    {"name": "前端", "slug": "frontend", "color": "#FF7300"},
    {"name": "后端", "slug": "backend", "color": "#3C5AA6"},
    {"name": "CSS", "slug": "css", "color": "#264de4"},
    {"name": "数据库", "slug": "database", "color": "#336791"},
    {"name": "DevOps", "slug": "devops", "color": "#FF6B6B"},
    # 杂项
    {"name": "像素艺术", "slug": "pixel-art", "color": "#FFDE00"},
    {"name": "游戏开发", "slug": "game-dev", "color": "#FF0000"},
    {"name": "机器学习", "slug": "ml", "color": "#FF6F00"},
    {"name": "区块链", "slug": "blockchain", "color": "#121D33"},
    {"name": "生活", "slug": "life", "color": "#9CBB0F"},
    {"name": "摄影", "slug": "photography", "color": "#E91E63"},
]

DEX_GENRES = [
    {"name": "冒险", "slug": "adventure", "color": "#FF6B6B"},
    {"name": "奇幻", "slug": "fantasy", "color": "#4ECDC4"},
    {"name": "犯罪", "slug": "crime", "color": "#45B7D1"},
    {"name": "剧情", "slug": "drama", "color": "#96CEB4"},
    {"name": "RPG", "slug": "rpg", "color": "#FFEAA7"},
    {"name": "动作RPG", "slug": "action-rpg", "color": "#F7DC6F"},
    {"name": "开放世界", "slug": "open-world", "color": "#BB8FCE"},
    {"name": "爱情", "slug": "romance", "color": "#85C1E9"},
    {"name": "科幻", "slug": "sci-fi", "color": "#F1948A"},
    {"name": "悬疑", "slug": "mystery", "color": "#7FB3D5"},
    {"name": "动作冒险", "slug": "action-adventure", "color": "#82E0AA"},
    {"name": "史诗", "slug": "epic", "color": "#F8C471"},
    {"name": "黑暗奇幻", "slug": "dark-fantasy", "color": "#85929E"},
    {"name": "回合制", "slug": "turn-based", "color": "#A3E4D7"},
    {"name": "前卫摇滚", "slug": "progressive-rock", "color": "#D7BDE2"},
    {"name": "另类摇滚", "slug": "alternative-rock", "color": "#DDA0DD"},
    {"name": "动画", "slug": "anime", "color": "#FF69B4"},
    {"name": "搞笑", "slug": "comedy", "color": "#FFD700"},
    {"name": "恐怖", "slug": "horror", "color": "#4A4A4A"},
    {"name": "战争", "slug": "war", "color": "#8B4513"},
    {"name": "历史", "slug": "history", "color": "#CD853F"},
    {"name": "纪录片", "slug": "documentary", "color": "#2E8B57"},
]

DEX_CATEGORIES = ['anime', 'movie', 'tv', 'game', 'book', 'music', 'other']
DEX_STATUSES = ['completed', 'watching', 'playing',
                'reading', 'listening', 'doing', 'dropped', 'planned']

MEDIA_TYPES = ['book', 'audio', 'image', 'video']

MEDIA_TAGS = [
    {"name": "风景", "slug": "landscape", "color": "#4CAF50"},
    {"name": "人物", "slug": "portrait", "color": "#FF9800"},
    {"name": "截图", "slug": "screenshot", "color": "#2196F3"},
    {"name": "图标", "slug": "icon", "color": "#9C27B0"},
    {"name": "背景", "slug": "background", "color": "#607D8B"},
    {"name": "素材", "slug": "asset", "color": "#795548"},
    {"name": "设计稿", "slug": "design", "color": "#E91E63"},
    {"name": "音乐", "slug": "music", "color": "#FF5722"},
    {"name": "音效", "slug": "sfx", "color": "#00BCD4"},
    {"name": "配音", "slug": "voice", "color": "#8BC34A"},
    {"name": "视频素材", "slug": "video-asset", "color": "#3F51B5"},
    {"name": "动画", "slug": "animation", "color": "#FFC107"},
]


# ============================================================
# 辅助函数
# ============================================================

def random_date(start_year: int = 2023, end_year: int = 2026) -> str:
    """生成 YYYY-MM-DD 格式随机日期"""
    start = datetime(start_year, 1, 1, tzinfo=timezone.utc)
    end = datetime(end_year, 6, 1, tzinfo=timezone.utc)
    delta = end - start
    random_days = random.randint(0, delta.days)
    return (start + timedelta(days=random_days)).strftime('%Y-%m-%d')


def generate_slug(text: str) -> str:
    """从中文标题生成英文 slug"""
    # 用 faker 生成英文词组的 slug，避免依赖 pypinyin
    words = fake.words(nb=random.randint(2, 5), unique=True)
    return '-'.join(words).lower() + f'-{random.randint(100, 999)}'


def generate_markdown_content(min_sections: int = 3, max_sections: int = 6) -> str:
    """生成随机 Markdown 文章内容"""
    sections = []
    for _ in range(random.randint(min_sections, max_sections)):
        heading = f"{'#' * random.randint(2, 3)} {fake.sentence(nb_words=4)}"
        paragraphs = []
        for _ in range(random.randint(2, 5)):
            paragraphs.append(fake.paragraph(
                nb_sentences=random.randint(3, 8)))

        # 随机插入代码块、列表或引用
        extra = ""
        roll = random.random()
        if roll < 0.3:
            lang = random.choice(
                ['python', 'typescript', 'javascript', 'rust', 'go', 'bash', 'css', 'html'])
            code = '\n'.join(' '.join(fake.words(nb=random.randint(3, 8)))
                             for _ in range(random.randint(3, 6)))
            extra = f"\n\n```{lang}\n{code}\n```\n"
        elif roll < 0.5:
            items = '\n'.join(
                f"- {fake.sentence(nb_words=4)}" for _ in range(random.randint(3, 6)))
            extra = f"\n\n{items}\n"
        elif roll < 0.6:
            extra = f"\n\n> {fake.paragraph(nb_sentences=2)}\n"

        sections.append(f"{heading}\n\n{chr(10).join(paragraphs)}{extra}")

    result = '\n\n---\n\n'.join(sections)

    # 可选：加一张随机图片
    if random.random() < 0.4:
        result += f"\n\n![{fake.word()}](https://picsum.photos/seed/{fake.word()}/800/400)\n"

    return result


def calculate_reading_time(content: str) -> int:
    """估算阅读时间（分钟）"""
    if not content:
        return 0
    content_without_code = re.sub(r'```[\s\S]*?```', '', content)
    text = re.sub(r'[#*`\[\]>\-]', '', content_without_code)
    char_count = len(text.strip())
    return max(1, round(char_count / 300) + content.count('![') // 2)


# ============================================================
# 播种函数
# ============================================================

async def seed_categories(db: AsyncSession) -> dict[str, str]:
    cat_map = {}
    for c in CATEGORIES:
        obj = PostCategory(name=c["name"], slug=c["slug"],
                           icon=c.get("icon"), color=c.get("color"))
        db.add(obj)
        await db.flush()
        cat_map[c["name"]] = obj.id
    await db.commit()
    print(f"✅ 导入 {len(CATEGORIES)} 个文章分类")
    return cat_map


async def seed_tags(db: AsyncSession) -> dict[str, str]:
    tag_map = {}
    for t in TAGS:
        obj = PostTag(name=t["name"], slug=t["slug"], color=t.get("color"))
        db.add(obj)
        await db.flush()
        tag_map[t["name"]] = obj.id
    await db.commit()
    print(f"✅ 导入 {len(TAGS)} 个文章标签")
    return tag_map


async def seed_posts(db: AsyncSession, cat_map: dict[str, str], tag_map: dict[str, str], count: int = 100):
    tag_names = list(tag_map.keys())
    post_titles = set()

    for i in range(count):
        # 生成不重复标题
        while True:
            title = fake.sentence(nb_words=random.randint(4, 10)).rstrip('.')
            if title not in post_titles:
                post_titles.add(title)
                break

        slug = generate_slug(title)
        description = fake.paragraph(nb_sentences=2)
        content = generate_markdown_content()
        reading_time = calculate_reading_time(content)
        word_count = len(content.strip())

        created = random_date(2023, 2026)
        published = random.random() < 0.85
        featured = published and random.random() < 0.15
        views = random.randint(0, 5000)
        category_name = random.choice(list(cat_map.keys()))
        post_tags = random.sample(tag_names, k=random.randint(1, 5))

        post = Post(
            slug=slug,
            title=title,
            description=description,
            content=content,
            cover_image=f"https://picsum.photos/seed/{slug}/800/400",
            created_at=datetime.strptime(
                created, '%Y-%m-%d').replace(tzinfo=timezone.utc),
            published=published,
            featured=featured,
            reading_time=reading_time,
            word_count=word_count,
            views=views,
            category_id=cat_map[category_name],
        )
        db.add(post)
        await db.flush()

        for tag_name in post_tags:
            await db.execute(
                post_to_post_tags.insert().values(
                    post_id=post.id, post_tag_id=tag_map[tag_name])
            )

        if (i + 1) % 20 == 0:
            await db.commit()
            print(f"  ⏳ 已导入 {i + 1}/{count} 篇文章...")

    await db.commit()
    print(f"✅ 导入 {count} 篇文章")


async def seed_dex_genres(db: AsyncSession) -> dict[str, str]:
    genre_map = {}
    for g in DEX_GENRES:
        obj = DexGenre(name=g["name"], slug=g["slug"], color=g["color"])
        db.add(obj)
        await db.flush()
        genre_map[g["name"]] = obj.id
    await db.commit()
    print(f"✅ 导入 {len(DEX_GENRES)} 个图鉴题材")
    return genre_map


async def seed_dex_entries(db: AsyncSession, genre_map: dict[str, str], count: int = 50):
    genre_names = list(genre_map.keys())
    titles = set()

    category_title_templates = {
        'anime': ['{name}', '{name} 第二季', '{name} 剧场版', '{name} 特别篇'],
        'movie': ['{name}', '{name} 2', '{name}：新篇章'],
        'tv': ['{name}', '{name} 第二季', '{name} 第三季', '{name}：衍生剧'],
        'game': ['{name}', '{name} 2', '{name}：重制版', '{name}：终极版'],
        'book': ['{name}', '{name} 第二部', '{name} 第三部', '{name}：全本'],
        'music': ['{name}', 'The Best of {name}', '{name} Live'],
    }

    fake_en = Faker('en_US')

    for i in range(count):
        while True:
            name = fake.last_name() if random.random() < 0.5 else fake.word()
            title = name.title()
            if title not in titles:
                titles.add(title)
                break

        category = random.choice(DEX_CATEGORIES)
        slug = generate_slug(title)
        status = random.choice(DEX_STATUSES)
        rating = 0 if status in (
            'dropped', 'planned') else random.randint(1, 10)
        year = random.randint(1990, 2026)

        start = random_date(max(2000, year), 2026)
        finish = random_date(
            max(2000, year), 2026) if status == 'completed' else None

        entry = Dex(
            slug=slug,
            title=title,
            original_title=fake_en.catch_phrase() if random.random() < 0.6 else None,
            cover_image=f"https://picsum.photos/seed/{slug}/300/400",
            category=category,
            status=status,
            rating=rating,
            start_date=start,
            finish_date=finish,
            comment=fake.paragraph(
                nb_sentences=2) if random.random() < 0.7 else None,
            creator=fake.name() if random.random() < 0.8 else None,
            year=year,
            summary=fake.paragraph(
                nb_sentences=3) if random.random() < 0.5 else None,
        )
        db.add(entry)
        await db.flush()

        # 随机挂题材
        entry_genres = random.sample(genre_names, k=random.randint(1, 3))
        for gn in entry_genres:
            await db.execute(
                dex_to_dex_genres.insert().values(
                    dex_id=entry.id, dex_genre_id=genre_map[gn])
            )

        if (i + 1) % 20 == 0:
            await db.commit()
            print(f"  ⏳ 已导入 {i + 1}/{count} 个图鉴...")

    await db.commit()
    print(f"✅ 导入 {count} 个图鉴条目")


async def seed_media_tags(db: AsyncSession) -> dict[str, str]:
    tag_map = {}
    for t in MEDIA_TAGS:
        obj = MediaTag(name=t["name"], slug=t["slug"], color=t.get("color"))
        db.add(obj)
        await db.flush()
        tag_map[t["name"]] = obj.id
    await db.commit()
    print(f"✅ 导入 {len(MEDIA_TAGS)} 个媒体标签")
    return tag_map


def _generate_placeholder_file(mtype: str, ext: str) -> tuple[str, int, str, dict]:
    """生成占位文件，返回 (相对路径, 文件大小, mime类型, 元数据)"""
    from PIL import Image
    import mutagen

    year_dir = str(random.randint(2023, 2026))
    filename = f"{uuid.uuid4().hex}{ext}"
    rel_dir = f"uploads/media/{mtype}/{year_dir}"
    os.makedirs(rel_dir, exist_ok=True)
    save_path = os.path.join(rel_dir, filename)

    mime_map = {
        '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
        '.png': 'image/png', '.webp': 'image/webp',
        '.gif': 'image/gif',
        '.mp3': 'audio/mpeg', '.wav': 'audio/wav',
        '.ogg': 'audio/ogg', '.flac': 'audio/flac',
        '.mp4': 'video/mp4', '.webm': 'video/webm',
        '.mov': 'video/quicktime',
        '.pdf': 'application/pdf',
    }
    mime = mime_map.get(ext, 'application/octet-stream')
    metadata = {}

    if mtype == 'image':
        # 生成 200×150 的随机颜色占位图
        color = random.choice(['#EE1515', '#3B4CCA', '#FFDE00', '#4CAF50', '#FF7300', '#9CBB0F'])
        img = Image.new('RGB', (200, 150), color)
        img.save(save_path)
        metadata = {'width': 200, 'height': 150, 'format': ext.lstrip('.').upper(), 'mode': 'RGB'}

    elif mtype == 'audio':
        # 生成极简 WAV 占位（1秒静音）
        import struct
        import wave
        sample_rate = 44100
        duration = 1
        num_samples = sample_rate * duration
        # 生成极小幅度的白噪声
        samples = [random.randint(-100, 100) for _ in range(num_samples)]
        with wave.open(save_path, 'w') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            for s in samples:
                wf.writeframes(struct.pack('<h', s))
        metadata = {'duration': duration, 'bitrate': sample_rate * 16, 'channels': 1}

    elif mtype == 'video':
        # 视频占位就生成一张图片（无法真正生成视频）
        color = random.choice(['#333333', '#555555', '#777777'])
        img = Image.new('RGB', (320, 240), color)
        img.save(save_path)
        metadata = {'width': 320, 'height': 240, 'duration': 0}

    else:  # book — 生成空白 PDF
        from io import BytesIO
        pdf_content = b'%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]>>endobj\nxref\n0 4\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \ntrailer<</Size 4/Root 1 0 R>>\nstartxref\n190\n%%EOF'
        with open(save_path, 'wb') as f:
            f.write(pdf_content)
        metadata = {'pages': 1}

    file_size = os.path.getsize(save_path)
    return f"/{save_path}", file_size, mime, metadata


async def seed_media(db: AsyncSession, tag_map: dict[str, str], count: int = 30):
    tag_names = list(tag_map.keys())

    for i in range(count):
        mtype = random.choice(MEDIA_TYPES)
        ext_map = {
            'image': random.choice(['.jpg', '.png', '.webp', '.gif']),
            'audio': random.choice(['.wav']),  # 只用 wav，其他格式需要编码器
            'video': random.choice(['.jpg']),  # 假装视频，实际是图
            'book': '.pdf',
        }
        ext = ext_map[mtype]

        title = f"{fake.word()}_{uuid.uuid4().hex[:8]}{ext}"
        file_path, file_size, mime_type, metadata = _generate_placeholder_file(mtype, ext)

        media = Media(
            slug=generate_slug(title),
            title=title,
            file_path=file_path,
            file_size=file_size,
            mime_type=mime_type,
            media_type=mtype,
            extension=ext,
            meta_data=metadata,
        )
        db.add(media)
        await db.flush()

        # 随机挂标签
        for tag_name in random.sample(tag_names, k=random.randint(0, 3)):
            await db.execute(
                media_to_media_tags.insert().values(
                    media_id=media.id, media_tag_id=tag_map[tag_name])
            )

        if (i + 1) % 20 == 0:
            await db.commit()
            print(f"  ⏳ 已导入 {i + 1}/{count} 个媒体文件...")

    await db.commit()
    print(f"✅ 导入 {count} 个媒体文件（含磁盘占位文件）")


# ============================================================
# 主入口
# ============================================================

async def seed():
    await init_db()
    async with async_session() as db:
        # --- 清空 ---
        print("🧹 清空现有数据...")
        await db.execute(post_to_post_tags.delete())
        await db.execute(dex_to_dex_genres.delete())
        await db.execute(media_to_media_tags.delete())
        for tbl in [Post, PostTag, PostCategory, Dex, DexGenre, Media, MediaTag]:
            await db.execute(tbl.__table__.delete())
        await db.commit()
        print("✅ 数据清空完成\n")

        # --- 播种 ---
        cat_map = await seed_categories(db)
        tag_map = await seed_tags(db)
        await seed_posts(db, cat_map, tag_map, count=100)     # ← 改这里控制文章数量

        genre_map = await seed_dex_genres(db)
        await seed_dex_entries(db, genre_map, count=80)       # ← 改这里控制图鉴数量

        mt_map = await seed_media_tags(db)
        await seed_media(db, mt_map, count=30)                # ← 改这里控制媒体数量

        print("\n🎉 所有种子数据导入完成！")


if __name__ == "__main__":
    asyncio.run(seed())
