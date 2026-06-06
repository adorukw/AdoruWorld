import uuid

from sqlalchemy import Float, Integer, String, Text, Enum as SAEnum, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def _uuid():
    return str(uuid.uuid4())


DexCategoryEnum = SAEnum("anime", "movie", "tv", "game",
                         "book", "music", "other", name="dex_category_enum")

DexStatusEnum = SAEnum(
    "completed", "watching", "playing", "reading", "listening", "doing", "dropped", "planned",
    name="dex_status_enum",
)

dex_to_dex_genres = Table(
    "dex_to_dex_genres",
    Base.metadata,
    Column("dex_entry_id", String, ForeignKey(
        "dex_entries.id"), primary_key=True),
    Column("dex_genre_id", String, ForeignKey(
        "dex_genres.id"), primary_key=True)
)


class DexEntry(Base):
    __tablename__ = "dex_entries"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    original_title: Mapped[str | None] = mapped_column(String, nullable=True)
    cover_image: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[str] = mapped_column(DexCategoryEnum, nullable=False)
    status: Mapped[str] = mapped_column(DexStatusEnum, nullable=False)
    rating: Mapped[float] = mapped_column(Float, default=0.0)
    start_date: Mapped[str | None] = mapped_column(String, nullable=True)
    finish_date: Mapped[str | None] = mapped_column(String, nullable=True)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    creator: Mapped[str | None] = mapped_column(String, nullable=True)
    year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    
    genres: Mapped[list["DexGenre"]] = relationship(
        "DexGenre", secondary=dex_to_dex_genres, back_populates="dex_entries", lazy="selectin")
