# app/models/book.py
from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    author: Mapped[str] = mapped_column(String(200), nullable=False)

    # ISBNs vary (10 or 13, with hyphens sometimes); keep room.
    isbn: Mapped[str] = mapped_column(String(32), unique=True, index=True, nullable=False)

    # Store year as int; optional
    published_year: Mapped[int | None] = mapped_column(Integer, nullable=True)