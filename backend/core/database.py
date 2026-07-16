from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from backend.core.config import settings

# Create async engine for PostgreSQL
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True,
    pool_size=5,
    max_overflow=10,
)

# Async session factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for FastAPI that yields a database session.

    Commits once the request handler returns cleanly; rolls back on any
    exception raised while handling the request (including a deliberate
    `HTTPException` from a router), so a 4xx/5xx response never leaves a
    half-applied write committed. Repositories should only ever call
    `flush()`/`refresh()` (to pull back generated UUIDs/timestamps
    mid-request) and never `commit()` themselves -- this is the one place
    that happens.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
