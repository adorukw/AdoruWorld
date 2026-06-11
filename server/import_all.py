"""
import_all.py — AdoruWorld 全量数据导入脚本

作用：从 export_all.py 导出的 ZIP 包中恢复全部数据，
      包含 manifest.json（结构化数据）和 uploads/（媒体文件）。

用法：
    python import_all.py backup.zip                    # 恢复模式（保留 UUID）
    python import_all.py backup.zip --clear            # 清空数据库 + 文件后恢复
    python import_all.py backup.zip --clear --dry-run  # 预览模式，不实际写入
"""
import argparse
import asyncio
import json
import os
import shutil
import sys
import zipfile
from datetime import datetime
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
from sqlalchemy import insert, delete as sa_delete


# ── 日志 ──────────────────────────────────────────────────────

def info(msg: str):
    print(f"  ℹ️  {msg}")


def ok(msg: str):
    print(f"  ✅ {msg}")


def warn(msg: str):
    print(f"  ⚠️  {msg}")


# ── 清空数据库 ────────────────────────────────────────────────

async def clear_database(db):
    """按依赖顺序清空所有表数据"""
    info("清空关联表...")
    await db.execute(sa_delete(post_to_post_tags))
    await db.execute(sa_delete(dex_to_dex_genres))
    await db.execute(sa_delete(media_to_media_tags))

    info("清空主表（有依赖优先）...")
    await db.execute(sa_delete(Post.__table__))
    await db.execute(sa_delete(DexEntry.__table__))
    await db.execute(sa_delete(Media.__table__))

    info("清空主表（无依赖）...")
    await db.execute(sa_delete(PostCategory.__table__))
    await db.execute(sa_delete(PostTag.__table__))
    await db.execute(sa_delete(DexGenre.__table__))
    await db.execute(sa_delete(MediaTag.__table__))

    await db.commit()
    ok("数据库已清空")


def clear_uploads():
    """删除 server/uploads/ 下所有文件"""
    uploads_dir = SERVER_DIR / "uploads"
    if not uploads_dir.exists():
        return
    for item in uploads_dir.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()
    ok(f"已清空 uploads/ 目录")


# ── 提取 ZIP ──────────────────────────────────────────────────

def read_manifest(zip_path: str) -> tuple[dict, list[str]]:
    """读取 ZIP 中的 manifest.json，返回 (data, members)"""
    path = Path(zip_path)
    if not path.exists():
        print(f"❌ 文件不存在: {path}")
        sys.exit(1)

    print(f"\n📂 正在读取: {path}")
    with zipfile.ZipFile(path, "r") as zf:
        if "manifest.json" not in zf.namelist():
            print("❌ ZIP 中缺少 manifest.json，不是有效的导出文件")
            sys.exit(1)
        manifest = json.loads(zf.read("manifest.json"))

        version = manifest.get("version", "")
        if not version.startswith("1."):
            warn(f"未知的导出版本: {version}，尝试继续导入...")

        # 收集需要解压的文件列表
        members = [n for n in zf.namelist() if n != "manifest.json" and not n.startswith("__")]

    return manifest["data"], members


def extract_media_files(zip_path: str, members: list[str]):
    """从 ZIP 中提取媒体文件到 server 目录"""
    if not members:
        ok("无媒体文件需要解压")
        return
    info(f"解压 {len(members)} 个媒体文件...")
    with zipfile.ZipFile(zip_path, "r") as zf:
        for name in members:
            target = SERVER_DIR / name
            target.parent.mkdir(parents=True, exist_ok=True)
            zf.extract(name, SERVER_DIR)
    ok(f"已解压 {len(members)} 个媒体文件")


# ── 导入逻辑 ──────────────────────────────────────────────────

def _parse_dt(val):
    """字符串 → datetime，容错处理"""
    if not val:
        return None
    if isinstance(val, datetime):
        return val
    try:
        return datetime.fromisoformat(val)
    except (ValueError, TypeError):
        return None


async def import_data(db, data: dict, dry_run: bool):
    """按依赖顺序导入所有数据"""
    total_inserted = 0

    # ── 第一轮：无依赖的表 ──────────────────────────────────
    tables = [
        ("文章分类", "postCategories", PostCategory, []),
        ("文章标签", "postTags", PostTag, []),
        ("图鉴题材", "dexGenres", DexGenre, []),
        ("媒体标签", "mediaTags", MediaTag, []),
    ]

    for label, key, model, _ in tables:
        rows = data.get(key, [])
        if not rows:
            info(f"{label}: 0 条（无数据）")
            continue
        if dry_run:
            info(f"{label}: {len(rows)} 条（预览，不写入）")
            continue
        for row in rows:
            stmt = insert(model).values(**row)
            await db.execute(stmt)
        await db.commit()
        ok(f"{label}: 已导入 {len(rows)} 条")

    total_inserted += sum(len(data.get(k, [])) for _, k, _, _ in tables)

    # ── 第二轮：有依赖的表 ──────────────────────────────────
    # 文章
    posts = data.get("posts", [])
    if posts:
        if dry_run:
            info(f"文章: {len(posts)} 条（预览，不写入）")
        else:
            for post in posts:
                # 分离 tag 关联
                tag_ids = post.pop("_tagIds", [])

                # 处理时间字段
                if "created_at" in post:
                    post["created_at"] = _parse_dt(post["created_at"])
                if "updated_at" in post:
                    post["updated_at"] = _parse_dt(post["updated_at"])

                stmt = insert(Post).values(**post)
                await db.execute(stmt)

                # 写关联表
                for tag_id in tag_ids:
                    await db.execute(
                        insert(post_to_post_tags).values(
                            post_id=post["id"],
                            post_tag_id=tag_id,
                        )
                    )
            await db.commit()
            ok(f"文章: 已导入 {len(posts)} 条")
    else:
        info("文章: 0 条（无数据）")
    total_inserted += len(posts)

    # 图鉴条目
    entries = data.get("dexEntries", [])
    if entries:
        if dry_run:
            info(f"图鉴条目: {len(entries)} 条（预览，不写入）")
        else:
            for entry in entries:
                genre_ids = entry.pop("_genreIds", [])

                stmt = insert(DexEntry).values(**entry)
                await db.execute(stmt)

                for genre_id in genre_ids:
                    await db.execute(
                        insert(dex_to_dex_genres).values(
                            dex_entry_id=entry["id"],
                            dex_genre_id=genre_id,
                        )
                    )
            await db.commit()
            ok(f"图鉴条目: 已导入 {len(entries)} 条")
    else:
        info("图鉴条目: 0 条（无数据）")
    total_inserted += len(entries)

    # 媒体资源
    medias = data.get("medias", [])
    if medias:
        if dry_run:
            info(f"媒体资源: {len(medias)} 条（预览，不写入）")
        else:
            for media in medias:
                tag_ids = media.pop("_tagIds", [])

                if "uploaded_at" in media:
                    media["uploaded_at"] = _parse_dt(media["uploaded_at"])

                stmt = insert(Media).values(**media)
                await db.execute(stmt)

                for tag_id in tag_ids:
                    await db.execute(
                        insert(media_to_media_tags).values(
                            media_id=media["id"],
                            media_tag_id=tag_id,
                        )
                    )
            await db.commit()
            ok(f"媒体资源: 已导入 {len(medias)} 条")
    else:
        info("媒体资源: 0 条（无数据）")
    total_inserted += len(medias)

    return total_inserted


# ── 校验 ──────────────────────────────────────────────────────

def validate_manifest(data: dict) -> list[str]:
    """验证 manifest 数据完整性，返回警告列表"""
    warnings = []

    required_keys = [
        "postCategories", "postTags", "dexGenres", "mediaTags",
        "posts", "dexEntries", "medias",
    ]
    for key in required_keys:
        if key not in data:
            warnings.append(f"缺少数据段: {key}")

    # 检查 posts 引用的 category 是否存在
    category_ids = {c["id"] for c in data.get("postCategories", [])}
    tag_ids = {t["id"] for t in data.get("postTags", [])}
    for post in data.get("posts", []):
        cid = post.get("category_id")
        if cid and cid not in category_ids:
            warnings.append(f"文章 '{post.get('title', '?')}' 引用了不存在的分类 ID: {cid}")
        for tid in post.get("_tagIds", []):
            if tid not in tag_ids:
                warnings.append(f"文章 '{post.get('title', '?')}' 引用了不存在的标签 ID: {tid}")

    # 检查 dexEntries 引用的 genre 是否存在
    genre_ids = {g["id"] for g in data.get("dexGenres", [])}
    for entry in data.get("dexEntries", []):
        for gid in entry.get("_genreIds", []):
            if gid not in genre_ids:
                warnings.append(f"图鉴 '{entry.get('title', '?')}' 引用了不存在的题材 ID: {gid}")

    # 检查 medias 引用的 tag 是否存在
    media_tag_ids = {t["id"] for t in data.get("mediaTags", [])}
    for media in data.get("medias", []):
        for tid in media.get("_tagIds", []):
            if tid not in media_tag_ids:
                warnings.append(f"媒体 '{media.get('title', '?')}' 引用了不存在的标签 ID: {tid}")

    return warnings


def print_stats(data: dict):
    """打印数据统计"""
    stats = {
        "文章分类": len(data.get("postCategories", [])),
        "文章标签": len(data.get("postTags", [])),
        "图鉴题材": len(data.get("dexGenres", [])),
        "媒体标签": len(data.get("mediaTags", [])),
        "文章": len(data.get("posts", [])),
        "图鉴条目": len(data.get("dexEntries", [])),
        "媒体资源": len(data.get("medias", [])),
    }
    total = sum(stats.values())
    print("\n📊 待导入数据统计：")
    for name, count in stats.items():
        print(f"   {name}: {count} 条")
    print(f"   ──────────")
    print(f"   总计: {total} 条记录")


# ── 主入口 ────────────────────────────────────────────────────

async def import_main(zip_path: str, clear: bool, dry_run: bool):
    print("⭐ AdoruWorld 数据导入工具 ⭐")
    print("=" * 40)

    # 1. 读取 manifest & 文件列表
    data, members = read_manifest(zip_path)

    # 2. 打印统计
    print_stats(data)

    # 3. 校验完整性
    warnings = validate_manifest(data)
    if warnings:
        print(f"\n⚠️  发现 {len(warnings)} 个潜在问题：")
        for w in warnings:
            print(f"   ⚠️  {w}")
        if not dry_run:
            resp = input("\n  继续导入？(y/N): ").strip().lower()
            if resp != "y":
                print("🚫 已取消导入")
                return

    # 4. 初始化数据库
    await init_db()
    if dry_run:
        print("\n🔍 预览模式（不写入数据库）")
    else:
        print()

    async with async_session() as db:
        # 5. 清空（如果指定了 --clear）
        if clear:
            if dry_run:
                info("预览模式：将清空数据库（跳过）")
            else:
                await clear_database(db)
                clear_uploads()

        # 6. 解压媒体文件（清空后再解压，避免被删掉）
        if not dry_run:
            extract_media_files(zip_path, members)

        # 7. 导入数据
        print()
        total = await import_data(db, data, dry_run)

    if not dry_run:
        print(f"\n✅ 导入完成！共处理 {total} 条记录，媒体文件已恢复。")
    else:
        print(f"\n🔍 预览完成，未写入任何数据。使用 --clear 实际执行导入。")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AdoruWorld 全量数据导入")
    parser.add_argument("input", help="ZIP 文件路径（由 export_all.py 导出）")
    parser.add_argument("--clear", action="store_true", help="导入前清空现有数据库和上传文件")
    parser.add_argument("--dry-run", action="store_true", help="预览模式，不实际写入数据库")
    args = parser.parse_args()

    asyncio.run(import_main(args.input, args.clear, args.dry_run))
