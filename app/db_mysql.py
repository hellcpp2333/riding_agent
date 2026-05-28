import os

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.models import Base

MYSQL_USER = os.environ.get("MYSQL_USER", "root")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
MYSQL_HOST = os.environ.get("MYSQL_HOST", "127.0.0.1")
MYSQL_PORT = os.environ.get("MYSQL_PORT", "3306")
MYSQL_DB = os.environ.get("MYSQL_DB", "bike_route_planner")

DATABASE_URL = (
    f"mysql+aiomysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
    f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
)

engine: AsyncEngine | None = None
async_session_factory: async_sessionmaker[AsyncSession] | None = None


def init_mysql_engine() -> AsyncEngine:
    global engine, async_session_factory
    engine = create_async_engine(
        DATABASE_URL,
        pool_size=5,
        max_overflow=10,
        pool_recycle=3600,
        echo=False,
    )
    async_session_factory = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    return engine


async def init_db() -> None:
    assert engine is not None, "MySQL engine not initialized"
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def dispose_mysql() -> None:
    global engine, async_session_factory
    if engine:
        await engine.dispose()
        engine = None
        async_session_factory = None


async def get_db_session() -> AsyncSession:
    assert async_session_factory is not None, "Session factory not initialized"
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
