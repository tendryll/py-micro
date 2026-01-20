# app/dependencies/db.py
from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session


# Re-export a typed alias that reads nicely in endpoints/services
async def db_session() -> AsyncSession:
    # This is a small convenience wrapper when you prefer Depends(db_session)
    # If you prefer, you can depend on get_db_session directly.
    async for session in get_db_session():
        return session

    # Unreachable, but keeps mypy happy
    raise RuntimeError("Failed to acquire DB session")