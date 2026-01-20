from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session
from app.services.book_service import list_books, get_book_by_id, create_book

router = APIRouter()

@router.get("/")
async def get_books(db: AsyncSession = Depends(get_db_session)):
    return await list_books(db)