from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.books import BookModel
from src.schemas.books import BookSchema, BookGetSchema


class BookService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def setup_database(self, Base, engine):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        return {"success": True}

    async def add_book(self, book: BookSchema) -> BookSchema:
        new_book = BookModel(
            title=book.title,
            author=book.author
        )
        self.session.add(new_book)
        await self.session.commit()
        return book

    async def get_books(self) -> list[BookGetSchema]:
        query = select(BookModel)
        result = await self.session.execute(query)
        books = result.scalars().all() 
        return books