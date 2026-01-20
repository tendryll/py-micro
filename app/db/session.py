# app/db/session.py
from __future__ import annotations

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

_engine: AsyncEngine | None = None
_sessionmaker: async_sessionmaker[AsyncSession] | None = None


def _require_database_url() -> str:
    if not settings.database_url:
        raise RuntimeError(
            "DATABASE_URL is not set. Example (Postgres): "
            "'postgresql+asyncpg://user:pass@localhost:5432/mydb' "
            "Example (SQLite): 'sqlite+aiosqlite:///./dev.db'"
        )
    return settings.database_url


def init_engine() -> None:
    """
    Call once at startup (lifespan) to initialize the engine and session factory.
    """
    global _engine, _sessionmaker
    if _engine is not None and _sessionmaker is not None:
        return

    db_url = _require_database_url()

    _engine = create_async_engine(
        db_url,
        echo=settings.debug,  # ok for dev; keep False in prod
        pool_pre_ping=True,
    )
    _sessionmaker = async_sessionmaker(
        bind=_engine,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )


def get_engine() -> AsyncEngine:
    if _engine is None:
        raise RuntimeError("DB engine not initialized. Call init_engine() at startup.")
    return _engine


def get_sessionmaker() -> async_sessionmaker[AsyncSession]:
    if _sessionmaker is None:
        raise RuntimeError("Sessionmaker not initialized. Call init_engine() at startup.")
    return _sessionmaker


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency-friendly session generator.
    """
    session_factory = get_sessionmaker()
    async with session_factory() as session:
        yield session


async def dispose_engine() -> None:
    """
    Call once at shutdown (lifespan) to close connections.
    """
    global _engine
    if _engine is not None:
        await _engine.dispose()
        _engine = None