from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.books import BookModel
from src.schemas.books import BookPatchSchema, BookSchema, BookGetSchema, BookUpdateSchema


class BookService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def setup_database(self, Base, engine):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        return {"success": True}

    async def add_book(self, book: BookSchema) -> BookSchema:
        new_book = BookModel(                                         #??????????????
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
    
    async def get_book(self, book_id: int):
        query = select(BookModel).where(BookModel.id == book_id)
        result = await self.session.execute(query)
        book = result.scalars().first()
        return book
    
    async def delete_book(self, book_id: int):
        query = select(BookModel).where(BookModel.id == book_id)
        result = await self.session.execute(query)
        book = result.scalars().first()

        await self.session.delete(book)
        await self.session.commit()
        return {"messenge": f"Book id={book_id} deleted"}
    
    async def put_book(self, book: BookUpdateSchema):
        if book.id is None:
            new_book = BookSchema(
                title=book.title,
                author=book.author 
                )
            return await self.add_book(new_book)
        
        query = select(BookModel.id)
        result = await self.session.execute(query)
        books = result.scalars().all() 
        if book.id in books:
            await self.delete_book(book.id)

        new_book = BookModel(
            id=book.id,                                    
            title=book.title,
            author=book.author
        )
        self.session.add(new_book)
        await self.session.commit()
        return book
    
    async def update_book(self, book_id: int, book_data: BookPatchSchema):
        query = select(BookModel).where(BookModel.id == book_id)
        result = await self.session.execute(query)
        db_book = result.scalar_one_or_none()

        if not db_book:
            return None

        update_data = book_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_book, field, value)

        await self.session.commit()
        await self.session.refresh(db_book)

        return db_book