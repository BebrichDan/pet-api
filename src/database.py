from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

SQL_LITE = "sqlite+aiosqlite:///mydb.db"
POSTGRE_SQL = "postgresql+asyncpg://myuser:mypassword@localhost/mydb"

engine = create_async_engine(
    POSTGRE_SQL,
    echo=True
)

new_async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_async_session() as session:
        yield session

class Base(DeclarativeBase):         #??
    pass