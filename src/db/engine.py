from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio.session import  async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import AsyncGenerator
from src.config import Config


engine = create_async_engine(url=Config.DATABASE_URL,echo=True)
as_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with as_session() as session:
        yield session