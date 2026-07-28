from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from app.core.database import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.modules.dex.model import Dex


def _uuid():
    return str(uuid.uuid4())


class DexGenre(Base):
    __tablename__ = "dex_genres"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    color: Mapped[str | None] = mapped_column(String, nullable=False)

    dexs: Mapped[list[Dex]] = relationship(
        "Dex", secondary="dex_to_dex_genres", back_populates="genres"
    )
