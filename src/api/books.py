from fastapi import APIRouter, HTTPException

from src.api.dependencies import SessionDep
from src.schemas.books import BookGetSchema, BookPatchSchema, BookSchema, BookUpdateSchema
from src.services.book_service import BookService
from src.database import Base, engine


router = APIRouter()

@router.post("/setup")
async def setup_database(session: SessionDep):
    service = BookService(session)
    return await service.setup_database(Base, engine)

@router.post("/books", response_model=BookGetSchema)
async def add_book(book: BookSchema, session: SessionDep):
    service = BookService(session)
    return await service.add_book(book)

@router.get("/books", response_model=list[BookGetSchema])
async def get_books(session: SessionDep):
    service = BookService(session)
    return await service.get_books()

@router.get("/books/{book_id}", response_model=BookGetSchema)
async def get_book(session: SessionDep, book_id: int):
    service = BookService(session)
    book = await service.get_book(book_id)
    if not book:
        raise HTTPException(404, "Book not found")
    return book

@router.delete("/books/{book_id}", status_code=204)
async def delete_book(session: SessionDep, book_id: int):
    service = BookService(session)
    ok = await service.delete_book(book_id)
    if not ok:
        raise HTTPException(404, "Book not found")
    return None

@router.put("/books", response_model=BookGetSchema)
async def put_book(book: BookUpdateSchema, session: SessionDep):
    service = BookService(session)
    return await service.put_book(book)

@router.patch("/books/{book_id}", response_model=BookGetSchema)
async def update_book(book_id: int, book: BookPatchSchema, session: SessionDep):
    service = BookService(session)
    updated = await service.update_book(book_id, book)
    if not updated:
        raise HTTPException(404, "Book not found")
    return updated