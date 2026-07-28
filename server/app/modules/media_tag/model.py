from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from app.core.database import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.modules.media.model import Media


def _uuid():
    return str(uuid.uuid4())


class MediaTag(Base):
    __tablename__ = "media_tags"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    color: Mapped[str | None] = mapped_column(String, nullable=True)

    medias: Mapped[list[Media]] = relationship(
        "Media", secondary="media_to_media_tags", back_populates="tags"
    )
