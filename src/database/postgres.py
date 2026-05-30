"""Асинхронный движок и сессия PostgreSQL."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from core.config import settings

engine = create_async_engine(settings.postgres_url, echo=settings.debug)

session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    """Базовый класс для всех PostgreSQL моделей."""


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI Depends: выдаёт сессию, закрывает при выходе."""
    async with session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
