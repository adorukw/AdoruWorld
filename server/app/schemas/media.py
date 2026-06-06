from pydantic import BaseModel, Field
from app.schemas.media_tag import MediaTagResponse
from typing import Any
from datetime import datetime


class MediaCreate(BaseModel):
    """
    创建媒体
    - file_path 由上传接口返回
    - metadata_ 按媒体类型动态填写
    """
    slug: str
    title: str
    file_path: str = Field(..., alias="filePath")
    file_size: int = Field(..., alias="fileSize")
    mime_type: str = Field(..., alias="mimeType")
    media_type: str = Field(..., alias="mediaType")
    meta_data: dict[str, Any] = Field(default_factory=dict, alias="metaData")
    tag_ids: list[str] = Field(default_factory=list, alias="tagIds")

    model_config = {"populate_by_name": True}


class MediaUpdate(BaseModel):
    """更新媒体（全字段可选）"""
    title: str | None = None
    meta_data: dict[str, Any] | None = Field(None, alias="metaData")
    tag_ids: list[str] | None = Field(None, alias="tagIds")

    model_config = {"populate_by_name": True}


class MediaResponse(BaseModel):
    """媒体详情响应"""
    id: str
    slug: str
    title: str
    file_path: str = Field(..., alias="filePath")
    file_size: int = Field(..., alias="fileSize")
    media_type: str = Field(..., alias="mediaType")
    mime_type: str = Field(..., alias="mimeType")
    extension: str
    meta_data: dict[str, Any] = Field(default_factory=dict, alias="metaData")
    uploaded_at: datetime = Field(..., alias="uploadedAt")
    tags: list["MediaTagResponse"]

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }


class MediaUploadResponse(BaseModel):
    file_path: str = Field(..., alias="filePath")
    file_size: int = Field(..., alias="fileSize")
    mime_type: str = Field(..., alias="mimeType")
    extension: str
    media_type: str = Field(..., alias="mediaType")
    metadata: dict = {}

    model_config = {"populate_by_name": True}
