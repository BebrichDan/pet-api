from fastapi import APIRouter

from src.api.dependencies import SessionDep
from src.schemas.books import BookGetSchema, BookSchema
from src.services.book_service import BookService
from src.database import Base, engine


router = APIRouter()

@router.post("/setup")
async def setup_database(session: SessionDep):
    service = BookService(session)
    return await service.setup_database(Base, engine)

@router.post("/books")
async def add_book(book: BookSchema, session: SessionDep) -> BookSchema:
    service = BookService(session)
    return await service.add_book(book)

@router.get("/books")
async def get_books(session: SessionDep) -> list[BookGetSchema]:
    service = BookService(session)
    return await service.get_books()