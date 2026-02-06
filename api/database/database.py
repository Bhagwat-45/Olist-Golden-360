from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker,AsyncSession
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator
from api.config.settings import settings

class Base(DeclarativeBase):
    pass

engine = create_async_engine(
    settings.database_url,
    echo=False,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db() -> AsyncGenerator[AsyncSession,None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()