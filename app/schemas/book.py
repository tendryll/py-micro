# app/schemas/book.py
from __future__ import annotations

from pydantic import BaseModel, Field


class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=200)
    isbn: str = Field(min_length=10, max_length=32)
    published_year: int | None = Field(default=None, ge=0, le=3000)


class BookRead(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    published_year: int | None = None

    model_config = {"from_attributes": True}