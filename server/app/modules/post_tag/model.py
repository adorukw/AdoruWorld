from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from app.core.database import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.modules.post.model import Post


def _uuid():
    return str(uuid.uuid4())


class PostTag(Base):
    __tablename__ = "post_tags"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    name: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str | None] = mapped_column(String, nullable=True)
    color: Mapped[str | None] = mapped_column(String, nullable=True)

    posts: Mapped[list[Post]] = relationship(
        secondary="post_to_post_tags", back_populates="tags", lazy="selectin"
    )
