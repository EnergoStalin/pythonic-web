from typing import Annotated, TypeVar

from api.common.utils.env import genv
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

T = TypeVar("T")
_engine: AsyncEngine | None = None


def create_db_url():
    user = genv("POSTGRES_USER", "app")
    password = genv("POSTGRES_PASSWORD", "1234")
    host = genv("POSTGRES_HOST", "127.0.0.1")
    port = genv("POSTGRES_PORT", "5432")
    database = genv("POSTGRES_DB", "general")

    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"


async def init():
    engine = create_async_engine(create_db_url(), echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
    global _engine
    _engine = engine


async def close():
    if not _engine:
        raise ValueError("DB connection is None")
    await _engine.dispose()


async def get_db():
    if not _engine:
        raise ValueError("DB connection is None")
    async with AsyncSession(_engine, expire_on_commit=False) as session:
        yield session


DBST = AsyncSession
DB = Annotated[DBST, Depends(get_db)]

__all__ = ["init", "close", "get_db", "DB", "DBST"]
