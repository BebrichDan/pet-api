from fastapi import APIRouter

from src.api.books import router as book_router

main_router = APIRouter()

main_router.include_router(book_router)