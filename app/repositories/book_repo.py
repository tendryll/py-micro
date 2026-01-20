# app/repositories/book_repo.py
from __future__ import annotations

from typing import Sequence

from sqlalchemy import Select, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.book import Book


class BookRepo:
    """
    Repository layer: only talks to the database.
    No FastAPI imports. No HTTP exceptions. No business rules.
    """

    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    def _base_select(self) -> Select[tuple[Book]]:
        return select(Book)

    async def list_books(self, *, limit: int = 100, offset: int = 0) -> Sequence[Book]:
        stmt = (
            self._base_select()
            .order_by(Book.id.asc())
            .limit(limit)
            .offset(offset)
        )
        result = await self._db.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, book_id: int) -> Book | None:
        stmt = self._base_select().where(Book.id == book_id)
        result = await self._db.execute(stmt)
        return result.scalars().first()

    async def get_by_isbn(self, isbn: str) -> Book | None:
        stmt = self._base_select().where(Book.isbn == isbn)
        result = await self._db.execute(stmt)
        return result.scalars().first()

    async def create(
        self,
        *,
        title: str,
        author: str,
        isbn: str,
        published_year: int | None,
    ) -> Book:
        book = Book(
            title=title,
            author=author,
            isbn=isbn,
            published_year=published_year,
        )
        self._db.add(book)

        # Flush ensures:
        # - DB constraints (e.g., unique ISBN) are checked early
        # - PK id is assigned (for many DBs)
        await self._db.flush()
        return book

    async def delete_by_id(self, book_id: int) -> bool:
        """
        Returns True if a row was deleted.
        """
        stmt = delete(Book).where(Book.id == book_id)
        result = await self._db.execute(stmt)
        return (result.rowcount or 0) > 0