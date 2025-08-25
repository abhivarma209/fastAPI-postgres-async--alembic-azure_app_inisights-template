from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncEngine
from sqlalchemy.orm import declarative_base
from config import settings

Base = declarative_base()
engine: AsyncEngine | None = None
AsyncSessionFactory: async_sessionmaker | None = None


async def connect_to_db() -> None:
    """Initialize database engine and session factory."""
    global engine, AsyncSessionFactory
    engine = create_async_engine(
        settings.asyncpg_url,
        future=True,
        echo=True,
    )
    AsyncSessionFactory = async_sessionmaker(
        engine,
        autoflush=False,
        expire_on_commit=False,
    )
    # Optionally test connection
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def disconnect_from_db() -> None:
    """Dispose database engine."""
    global engine
    if engine:
        await engine.dispose()


# Dependency for FastAPI routes
async def get_db() -> AsyncGenerator:
    async with AsyncSessionFactory() as session:
        yield session
