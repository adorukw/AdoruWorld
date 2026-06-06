from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
import os
import uuid
from PIL import Image
import mutagen
import json

from app.database import get_db
from app.crud import medias as crud
from app.schemas import (
    MediaCreate, MediaUpdate, MediaResponse, MediaUploadResponse
)
from app.models import Media

router = APIRouter(prefix="/medias", tags=["medias"])


def analyze_file_metadata(file_path: str, media_type: str) -> dict:
    """自动分析文件元数据"""
    metadata = {}

    try:
        if media_type == "image":
            with Image.open(file_path) as img:
                metadata.update({
                    "width": img.width,
                    "height": img.height,
                    "format": img.format,
                    "mode": img.mode
                })

        elif media_type == "audio":
            try:
                audio = mutagen.File(file_path)
                if audio:
                    metadata.update({
                        "duration": int(audio.info.length) if hasattr(audio.info, 'length') else 0,
                        "bitrate": getattr(audio.info, 'bitrate', 0),
                        "channels": getattr(audio.info, 'channels', 0)
                    })

                    # 提取 ID3 标签
                    if hasattr(audio, 'tags') and audio.tags:
                        for key, value in audio.tags.items():
                            if isinstance(value, list) and value:
                                metadata[key.lower()] = str(value[0])
            except Exception as e:
                print(f"音频分析失败: {e}")

        elif media_type == "book":
            # 对于电子书，可以后续用 ebooklib 等库分析
            metadata.update({
                "pages": 0,  # 需要专门的库来分析
                "chapters": 0
            })

    except Exception as e:
        print(f"元数据提取失败: {e}")

    return metadata


@router.post("/upload", response_model=MediaUploadResponse)
async def upload_media(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    allowed_extensions = {
        ".jpg", ".jpeg", ".png", ".gif", ".webp",   # image
        ".mp3", ".wav", ".flac",                    # audio
        ".pdf", ".epub", ".mobi"                    # book
    }
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="不支持的文件类型")

    if ext in {".jpg", ".jpeg", ".png", ".gif", ".webp"}:
        media_type = "image"
    elif ext in {".mp3", ".wav", ".flac"}:
        media_type = "audio"
    else:
        media_type = "book"

    filename = f"{uuid.uuid4().hex}{ext}"
    save_dir = f"uploads/media/{media_type}"
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, filename)

    with open(save_path, "wb") as f:
        content = await file.read()
        f.write(content)

    metadata = analyze_file_metadata(save_path, media_type)

    return MediaUploadResponse(
        file_path=f"/{save_path}",
        file_size=os.path.getsize(save_path),
        mime_type=file.content_type,
        extension=ext,
        media_type=media_type,
        metadata=metadata
    )


@router.get("", response_model=list[MediaResponse])
async def list_meida(
    media_type: str | None = None,
    tag_slug: str | None = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    return await crud.get_media(db, media_type, tag_slug, skip, limit)


@router.get("/slug/{media_slug}", response_model=MediaResponse)
async def get_media_by_slug(slug: str, db: AsyncSession = Depends(get_db)):
    media = await crud.get_media_by_slug(db, slug)
    if not media:
        raise HTTPException(status_code=404, detail="媒体不存在")
    return media


@router.get("/{media_id}", response_model=MediaResponse)
async def get_media_by_id(media_id: str, db: AsyncSession = Depends(get_db)):
    media = await crud.get_media_by_id(db, media_id)
    if not media:
        raise HTTPException(status_code=404, detail="媒体不存在")
    return media


@router.post("", response_model=MediaResponse, status_code=201)
async def create_media(data: MediaCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_media(db, data)


@router.put("/{media_id}", response_model=MediaResponse)
async def update_media(media_id: str, data: MediaUpdate,  db: AsyncSession = Depends(get_db)):
    media = await crud.get_media_by_id(db, media_id)
    if not media:
        raise HTTPException(status_code=404, detail="媒体未找到")
    return await crud.update_media(db, media, data)


@router.delete("/{media_id}", status_code=204)
async def delete_media(media_id: str, db: AsyncSession = Depends(get_db)):
    media = await crud.get_media_by_id(db, media_id)
    if not media:
        raise HTTPException(status_code=404, detail="媒体未找到")

    file_path = media.file_path.lstrip("/")  # 去掉开头的 /
    if os.path.exists(file_path):
        os.remove(file_path)
    await crud.delete_media(db, media)
