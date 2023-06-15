from functools import lru_cache

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncEngine, AsyncSession

from fastgql.settings import ServerSettings, get_server_settings


@lru_cache
def get_engine(database_url: str) -> AsyncEngine:
    return AsyncEngine(create_engine(database_url))


def get_sessionmaker(
    settings: ServerSettings | None = None,
) -> sessionmaker:
    settings = settings or get_server_settings()
    engine = get_engine(settings.database_url)
    return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_database(
    settings: ServerSettings | None = None,
) -> None:
    settings = settings or get_server_settings()
    engine = get_engine(settings.database_url)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


def is_unique_constraint_violation(exception: Exception) -> bool:
    return isinstance(exception, IntegrityError) and "unique constraint" in str(exception).lower()


def is_foreign_key_violation(exception: Exception) -> bool:
    return isinstance(exception, IntegrityError) and "foreign key constraint" in str(exception).lower()


def is_not_null_violation(exception: Exception) -> bool:
    return isinstance(exception, IntegrityError) and "null value in column" in str(exception).lower()


def is_check_violation(exception: Exception) -> bool:
    return isinstance(exception, IntegrityError) and "check constraint" in str(exception).lower()
