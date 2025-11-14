from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.books import BookModel
from src.schemas.books import BookPatchSchema, BookSchema, BookGetSchema, BookUpdateSchema


class BookService:  # -> ORM
    def __init__(self, session: AsyncSession):
        self.session = session

    async def setup_database(self, Base, engine):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    async def add_book(self, book: BookSchema) -> BookModel:
        new_book = BookModel(
            title=book.title,
            author=book.author
        )
        self.session.add(new_book)
        await self.session.commit()
        await self.session.refresh(new_book)
        return new_book

    async def get_books(self) -> list[BookModel]:
        result = await self.session.execute(select(BookModel))
        return result.scalars().all()

    async def get_book(self, book_id: int) -> BookModel | None:
        result = await self.session.execute(
            select(BookModel).where(BookModel.id == book_id)
        )
        return result.scalars().first()

    async def delete_book(self, book_id: int) -> bool:
        book = await self.get_book(book_id)
        if not book:
            return False
        await self.session.delete(book)
        await self.session.commit()
        return True

    async def put_book(self, book: BookUpdateSchema) -> BookModel:
        existing_book = await self.get_book(book.id)

        if existing_book:
            for field, value in book.model_dump(exclude_unset=True).items():
                setattr(existing_book, field, value)

            await self.session.commit()
            await self.session.refresh(existing_book)
            return existing_book

        new_book = BookModel(**book.model_dump())
        self.session.add(new_book)
        await self.session.commit()
        await self.session.refresh(new_book)
        return new_book

    async def update_book(self, book_id: int, book_data: BookPatchSchema):
        book = await self.get_book(book_id)
        if not book:
            return None

        update_data = book_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(book, field, value)

        await self.session.commit()
        await self.session.refresh(book)
        return book