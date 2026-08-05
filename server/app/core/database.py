import asyncio
from pathlib import Path

from alembic import command
from alembic.config import Config
from app.core.config import BASE_DIR, DATABASE_URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def _run_migrations():
    cfg = Config(str(BASE_DIR / "alembic.ini"))
    command.upgrade(cfg, "head")


async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    await asyncio.to_thread(_run_migrations)
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
