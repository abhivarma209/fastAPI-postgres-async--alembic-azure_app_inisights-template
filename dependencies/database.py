import logging
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncEngine
from sqlalchemy.orm import declarative_base
from config import settings

Base = declarative_base()
engine: AsyncEngine | None = None
AsyncSessionFactory: async_sessionmaker | None = None

# Logger using module name
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

async def connect_to_db() -> None:
    """Initialize the database engine and session factory."""
    global engine, AsyncSessionFactory
    try:
        logger.info("Initializing database engine...")
        engine = create_async_engine(
            settings.asyncpg_url,
            future=True,
            echo=False,  # Set True if you want raw SQL logs
        )
        AsyncSessionFactory = async_sessionmaker(
            engine,
            autoflush=False,
            expire_on_commit=False,
        )
        logger.info("Database engine and session factory initialized successfully.")
    except Exception as e:
        logger.exception("Failed to initialize database engine: %s", e)
        raise

async def disconnect_from_db() -> None:
    """Dispose the database engine."""
    global engine
    if engine:
        try:
            logger.info("Disposing database engine...")
            await engine.dispose()
            logger.info("Database engine disposed successfully.")
        except Exception as e:
            logger.exception("Error while disposing database engine: %s", e)
            raise

# Dependency for FastAPI routes
async def get_db() -> AsyncGenerator:
    if AsyncSessionFactory is None:
        logger.error("AsyncSessionFactory not initialized! Did you call connect_to_db()?")
        raise RuntimeError("Database not connected")
    async with AsyncSessionFactory() as session:
        yield session
