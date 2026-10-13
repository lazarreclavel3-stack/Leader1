"""Database configuration and session management."""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.pool import NullPool
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration from environment variables."""

    database_url: str
    database_pool_size: int = 5
    secret_key: str
    debug: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

engine: AsyncEngine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    pool_size=settings.database_pool_size,
    max_overflow=10,
    pool_pre_ping=True,
)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield a database session."""
    async with async_session() as session:
        yield session


async def init_db():
    """Initialize the database (run migrations)."""
    async with engine.begin() as conn:
        await conn.run_sync(lambda x: None)


async def close_db():
    """Close the database connection pool."""
    await engine.dispose()
