import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    String, Text, Integer, DateTime, JSON, ForeignKey, Enum as SAEnum
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Table, Column

from app.database import Base
from sqlalchemy import Enum as SAEnum
from app.models.media_tags import MediaTag

MediaTypeEnum = SAEnum(
    "image", "audio", "book", "video",
    name="media_type_enum"
)


def _uuid():
    return str(uuid.uuid4())


def _utcnow():
    return datetime.now(timezone.utc)


# ---------- 多对多关联表 ----------
media_to_media_tags = Table(
    "media_to_media_tags",
    Base.metadata,
    Column("media_id", String, ForeignKey(
        "media.id", ondelete="CASCADE"), primary_key=True),
    Column("media_tag_id", String, ForeignKey(
        "media_tags.id", ondelete="CASCADE"), primary_key=True)
)


class Media(Base):
    __tablename__ = "media"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)

    # 文件信息
    file_path: Mapped[str] = mapped_column(String, nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)
    media_type: Mapped[str] = mapped_column(MediaTypeEnum, nullable=False)
    mime_type: Mapped[str] = mapped_column(String, nullable=False)
    extension: Mapped[str] = mapped_column(
        String, nullable=False)  # e.g. .jpg, .mp3, .pdf, .avi

    # 扩展元数据（按类型自由扩展）
    meta_data: Mapped[dict] = mapped_column(JSON, default=dict)

    # 时间
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow)

    # 关联标签
    tags: Mapped[list["MediaTag"]] = relationship(
        "MediaTag",
        secondary=media_to_media_tags,
        lazy="selectin"
    )
