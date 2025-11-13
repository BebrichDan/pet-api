from fastapi import APIRouter

from src.api.dependencies import SessionDep
from src.schemas.books import BookGetSchema, BookPatchSchema, BookSchema, BookUpdateSchema
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

@router.get("/books/{book_id}")
async def get_book(session: SessionDep, book_id: int) -> list[BookGetSchema]:
    service = BookService(session)
    return await service.get_book(book_id)

@router.delete("/books/{book_id}")
async def delete_book(session: SessionDep, book_id: int):
    service = BookService(session)
    return await service.delete_book(book_id)

@router.put("/books")
async def put_book(book: BookUpdateSchema, session: SessionDep):
    service = BookService(session)
    return await service.put_book(book)

@router.patch("/books/{book_id}")
async def update_book(book_id: int, book: BookPatchSchema, session: SessionDep):
    service = BookService(session)
    return await service.update_book(book_id, book)