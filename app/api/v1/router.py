# app/api/v1/router.py
from fastapi import APIRouter

from app.api.v1.endpoints import health, books

router = APIRouter()

# ---- Health / system routes ----
router.include_router(
    health.router,
    tags=["health"],
)

# ---- User domain routes ----
router.include_router(
    books.router,
    prefix="/books",
    tags=["books"],
)