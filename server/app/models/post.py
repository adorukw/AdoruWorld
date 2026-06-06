import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from .post_tag import PostTag
from .post_category import PostCategory


def _utcnow():
    return datetime.now(timezone.utc)


def _uuid():
    return str(uuid.uuid4())


post_to_post_tags = Table(
    "post_to_post_tags",
    Base.metadata,
    Column("post_id", String, ForeignKey(
        "posts.id", ondelete="CASCADE"), primary_key=True),
    Column("post_tag_id", String, ForeignKey(
        "post_tags.id", ondelete="CASCADE"), primary_key=True)
)


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    slug: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    cover_image: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=_utcnow, onupdate=_utcnow)
    published: Mapped[bool] = mapped_column(Boolean, default=False)
    reading_time: Mapped[int] = mapped_column(Integer, default=0)
    word_count: Mapped[int] = mapped_column(Integer, default=0)
    views: Mapped[int] = mapped_column(Integer, default=0)
    featured: Mapped[bool] = mapped_column(Boolean, default=False)

    category_id: Mapped[str] = mapped_column(
        String, ForeignKey("post_categories.id", ondelete="SET NULL")
    )

    category: Mapped["PostCategory"] = relationship(
        back_populates="posts",
        lazy="selectin"
    )

    tags: Mapped[list["PostTag"]] = relationship(
        secondary=post_to_post_tags,
        back_populates="posts",
        lazy="selectin"
    )
