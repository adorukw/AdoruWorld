"""
export_all.py — AdoruWorld 全量数据导出脚本

作用：将所有数据（文章、图鉴、媒体、分类、标签等）导出为 ZIP 包，
      包含 manifest.json（结构化数据）和 uploads/（媒体文件）。

用法：
    python export_all.py                        # 默认输出到 exports/ 目录
    python export_all.py -o my-backup.zip       # 指定输出路径
"""
import argparse
import asyncio
import json
import os
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

# ── 让 Python 能找到 app 包 ──────────────────────────────────
SERVER_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SERVER_DIR))

from app.database import async_session, init_db
from app.models import (
    Post, PostCategory, PostTag, post_to_post_tags,
    DexEntry, DexGenre, dex_to_dex_genres,
    Media, MediaTag, media_to_media_tags,
)


# ── 工具函数 ──────────────────────────────────────────────────

def _row_to_dict(row):
    """把 SQLAlchemy Core Row 转成可 JSON 序列化的 dict"""
    if row is None:
        return None
    d = dict(row._mapping)
    for k, v in d.items():
        if isinstance(v, datetime):
            d[k] = v.isoformat()
        # SQLAlchemy JSON/dict 类型已经是 dict，直接保留
    return d


def _path_in_zip(file_path: str) -> str:
    """数据库里的 file_path (/uploads/xxx) → ZIP 中的相对路径"""
    return file_path.lstrip("/")


def _local_path(file_path: str) -> Path:
    """数据库里的 file_path → 服务器上的真实路径"""
    return SERVER_DIR / _path_in_zip(file_path)


# ── 核心导出逻辑 ──────────────────────────────────────────────

async def collect_data() -> dict:
    """从数据库读取所有数据，按依赖顺序收集为 dict"""
    data = {}

    async with async_session() as db:
        # 1. 无依赖的表 ── 先导出
        print("📦 正在导出文章分类...")
        rows = await db.execute(
            PostCategory.__table__.select().order_by(PostCategory.__table__.c.name)
        )
        data["postCategories"] = [_row_to_dict(r) for r in rows.fetchall()]

        print("📦 正在导出文章标签...")
        rows = await db.execute(
            PostTag.__table__.select().order_by(PostTag.__table__.c.name)
        )
        data["postTags"] = [_row_to_dict(r) for r in rows.fetchall()]

        print("📦 正在导出图鉴题材...")
        rows = await db.execute(
            DexGenre.__table__.select().order_by(DexGenre.__table__.c.name)
        )
        data["dexGenres"] = [_row_to_dict(r) for r in rows.fetchall()]

        print("📦 正在导出媒体标签...")
        rows = await db.execute(
            MediaTag.__table__.select().order_by(MediaTag.__table__.c.name)
        )
        data["mediaTags"] = [_row_to_dict(r) for r in rows.fetchall()]

        # 2. 有依赖的表 ── 后导出
        print("📦 正在导出文章...")
        rows = await db.execute(
            Post.__table__.select().order_by(Post.__table__.c.created_at.desc())
        )
        posts = [_row_to_dict(r) for r in rows.fetchall()]
        # 为每篇文章附加其 tag ids
        for post in posts:
            tag_rows = await db.execute(
                post_to_post_tags.select().where(
                    post_to_post_tags.c.post_id == post["id"]
                )
            )
            post["_tagIds"] = [r.post_tag_id for r in tag_rows.fetchall()]
        data["posts"] = posts

        print("📦 正在导出图鉴条目...")
        rows = await db.execute(
            DexEntry.__table__.select().order_by(DexEntry.__table__.c.title)
        )
        entries = [_row_to_dict(r) for r in rows.fetchall()]
        for entry in entries:
            genre_rows = await db.execute(
                dex_to_dex_genres.select().where(
                    dex_to_dex_genres.c.dex_entry_id == entry["id"]
                )
            )
            entry["_genreIds"] = [r.dex_genre_id for r in genre_rows.fetchall()]
        data["dexEntries"] = entries

        print("📦 正在导出媒体资源...")
        rows = await db.execute(
            Media.__table__.select().order_by(Media.__table__.c.title)
        )
        medias = [_row_to_dict(r) for r in rows.fetchall()]
        for media in medias:
            tag_rows = await db.execute(
                media_to_media_tags.select().where(
                    media_to_media_tags.c.media_id == media["id"]
                )
            )
            media["_tagIds"] = [r.media_tag_id for r in tag_rows.fetchall()]
        data["medias"] = medias

    return data


def build_manifest(data: dict) -> dict:
    """构建完整 manifest"""
    return {
        "version": "1.0",
        "exportedAt": datetime.now(timezone.utc).isoformat(),
        "project": "AdoruWorld",
        "data": data,
    }


def add_media_files(zf: zipfile.ZipFile, data: dict):
    """把媒体文件加入 ZIP（只加 Media 表里记录的）"""
    added = set()
    for media in data.get("medias", []):
        fp = media.get("file_path", "")
        if not fp:
            continue
        zip_path = _path_in_zip(fp)
        if zip_path in added:
            continue
        local = _local_path(fp)
        if local.exists():
            zf.write(local, zip_path)
            added.add(zip_path)
            print(f"  ✅ 已打包: {zip_path}")
        else:
            print(f"  ⚠️  文件不存在，跳过: {local}")

    # 额外检查 Post cover_image 是否指向本地文件
    for post in data.get("posts", []):
        cover = post.get("cover_image", "") or ""
        if not cover.startswith("/"):
            continue  # 是 URL，跳过
        zip_path = _path_in_zip(cover)
        if zip_path in added:
            continue
        local = _local_path(cover)
        if local.exists():
            zf.write(local, zip_path)
            added.add(zip_path)
            print(f"  ✅ 已打包(封面): {zip_path}")
        else:
            print(f"  ⚠️  封面文件不存在，跳过: {local}")

    # 额外检查 DexEntry cover_image
    for entry in data.get("dexEntries", []):
        cover = entry.get("cover_image", "") or ""
        if not cover.startswith("/"):
            continue
        zip_path = _path_in_zip(cover)
        if zip_path in added:
            continue
        local = _local_path(cover)
        if local.exists():
            zf.write(local, zip_path)
            added.add(zip_path)
            print(f"  ✅ 已打包(图鉴封面): {zip_path}")
        else:
            print(f"  ⚠️  图鉴封面文件不存在，跳过: {local}")


def count_stats(data: dict) -> dict:
    """统计导出数据量"""
    return {
        "文章分类": len(data.get("postCategories", [])),
        "文章标签": len(data.get("postTags", [])),
        "图鉴题材": len(data.get("dexGenres", [])),
        "媒体标签": len(data.get("mediaTags", [])),
        "文章": len(data.get("posts", [])),
        "图鉴条目": len(data.get("dexEntries", [])),
        "媒体资源": len(data.get("medias", [])),
    }


# ── 主入口 ────────────────────────────────────────────────────

async def export(output_path: str):
    print("⭐ AdoruWorld 数据导出工具 ⭐")
    print("=" * 40)

    # 1. 收集数据
    await init_db()
    print("\n📖 正在读取数据库...")
    data = await collect_data()

    stats = count_stats(data)
    print("\n📊 导出统计：")
    for name, count in stats.items():
        print(f"   {name}: {count} 条")
    total = sum(stats.values())
    print(f"   ──────────")
    print(f"   总计: {total} 条记录")

    # 2. 构建 manifest
    manifest = build_manifest(data)
    manifest_json = json.dumps(manifest, ensure_ascii=False, indent=2)

    # 3. 写 ZIP
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    print(f"\n📦 正在打包 → {out} ...")

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        # 先写 manifest.json
        zf.writestr("manifest.json", manifest_json)
        print("  ✅ 已写入 manifest.json")

        # 再写媒体文件
        add_media_files(zf, data)

    size_mb = out.stat().st_size / 1024 / 1024
    print(f"\n✅ 导出完成！文件大小: {size_mb:.2f} MB")
    print(f"   📁 {out.resolve()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AdoruWorld 全量数据导出")
    parser.add_argument(
        "-o", "--output",
        default=str(SERVER_DIR / "exports" / f"adoruworld-export-{datetime.now().strftime('%Y-%m-%d')}.zip"),
        help="输出 ZIP 文件路径",
    )
    args = parser.parse_args()
    asyncio.run(export(args.output))
