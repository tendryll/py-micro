# app/services/book_service.py
from __future__ import annotations

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.book_repo import BookRepo
from app.schemas.book import BookCreate
from app.models.book import Book


def _normalize_isbn(isbn: str) -> str:
    """
    Normalize ISBN to reduce duplicates like:
      "978-1-234-56789-7" vs "9781234567897"
    Keep it simple: remove spaces and hyphens.
    """
    return isbn.replace("-", "").replace(" ", "").strip()


async def list_books(
    db: AsyncSession,
    *,
    limit: int = 100,
    offset: int = 0,
) -> list[Book]:
    repo = BookRepo(db)
    # Basic guardrails; service layer is a good place for these.
    limit = max(1, min(limit, 500))
    offset = max(0, offset)
    books = await repo.list_books(limit=limit, offset=offset)
    return list(books)


async def get_book_by_id(db: AsyncSession, book_id: int) -> Book | None:
    repo = BookRepo(db)
    return await repo.get_by_id(book_id)


async def create_book(db: AsyncSession, payload: BookCreate) -> Book:
    repo = BookRepo(db)

    isbn_norm = _normalize_isbn(payload.isbn)

    # Business rule: ISBN must be unique
    existing = await repo.get_by_isbn(isbn_norm)
    if existing:
        raise ValueError("A book with that ISBN already exists")

    try:
        book = await repo.create(
            title=payload.title.strip(),
            author=payload.author.strip(),
            isbn=isbn_norm,
            published_year=payload.published_year,
        )
        await db.commit()
        # Refresh so the returned instance has DB-populated fields
        await db.refresh(book)
        return book
    except IntegrityError as exc:
        # Handles race conditions where another request inserts same ISBN after our check
        await db.rollback()
        raise ValueError("A book with that ISBN already exists") from exc
    except Exception:
        await db.rollback()
        raise