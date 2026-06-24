"""
Database session management with SQLAlchemy async engine.
"""
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from app.infrastructure.config.settings import get_settings

settings = get_settings()

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_timeout=settings.DATABASE_POOL_TIMEOUT,
    pool_recycle=settings.DATABASE_POOL_RECYCLE,
    pool_pre_ping=True,
    # Use NullPool for testing
    poolclass=NullPool if settings.ENVIRONMENT == "test" else None,
)

# Session factory
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def init_db() -> None:
    """Initialize database connection."""
    # Import all models to register them
    from app.infrastructure.database.models import Base  # noqa: F401
    
    # Create tables (in development, use Alembic for migrations in production)
    if settings.ENVIRONMENT == "development":
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """Close database connections."""
    await engine.dispose()


@asynccontextmanager
async def get_db_session() -> AsyncSession:
    """Get a database session for dependency injection."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# Dependency for FastAPI
async def get_db() -> AsyncSession:
    """FastAPI dependency for database session."""
    async with get_db_session() as session:
        yield session