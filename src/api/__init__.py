from fastapi import APIRouter

from src.api.auth import router as auth_router
from src.api.books import router as book_router

main_router = APIRouter()

main_router.include_router(book_router)
main_router.include_router(auth_router)
