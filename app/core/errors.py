# app/core/errors.py
from __future__ import annotations


class AppError(Exception):
    """Base app error."""


class NotFoundError(AppError):
    pass


class ConflictError(AppError):
    pass


class UnauthorizedError(AppError):
    pass