# DATABASE_AGENT | 2026-05-10 | Async SQLAlchemy engine, session factory, startup helper
from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings
from app.models.base import Base

_is_sqlite = "sqlite" in settings.database_url

engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    connect_args={"check_same_thread": False} if _is_sqlite else {},
    # Prevent connection reuse for SQLite to avoid cross-session lock issues
    **{"pool_size": 1, "max_overflow": 0} if not _is_sqlite else {},
)

# Enable WAL mode and generous busy_timeout for SQLite
if _is_sqlite:

    @event.listens_for(engine.sync_engine, "connect")
    def set_sqlite_pragmas(dbapi_conn: object, _: object) -> None:
        cursor = dbapi_conn.cursor()  # type: ignore[union-attr]
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA busy_timeout=30000")  # wait up to 30s for locks
        cursor.close()


AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def create_all_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_all_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
