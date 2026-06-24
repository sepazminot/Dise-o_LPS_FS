"""
Pytest configuration and fixtures.
"""
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.infrastructure.database.models import Base


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def db_engine():
    """Create test database engine (SQLite in-memory for speed)."""
    from sqlalchemy.pool import StaticPool
    
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    await engine.dispose()


@pytest.fixture(scope="function")
async def db_session(db_engine):
    """Create test database session."""
    async_session = async_sessionmaker(
        db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    async with async_session() as session:
        yield session


@pytest.fixture(autouse=True)
def override_settings(monkeypatch):
    """Override settings for tests."""
    monkeypatch.setenv("ENVIRONMENT", "test")
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
    monkeypatch.setenv("REDIS_URL", "redis://localhost:***REMOVED***")
    monkeypatch.setenv("JWT_PRIVATE_KEY_PATH", "/tmp/test_private.pem")
    monkeypatch.setenv("JWT_PUBLIC_KEY_PATH", "/tmp/test_public.pem")