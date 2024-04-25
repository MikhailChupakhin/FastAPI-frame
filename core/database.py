# C:\Users\user1\PycharmProjects\FastAPi-actual\core\database.py
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from typing import AsyncGenerator
from core.config import settings

engine = create_async_engine(settings.db_settings.db_url())
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
