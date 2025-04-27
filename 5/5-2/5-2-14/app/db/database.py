"""Asynchronous database setup and session management for the application.

This module configures the async SQLAlchemy engine, session maker, and
provides a dependency for obtaining async sessions.
"""

from sqlalchemy.ext.asyncio import (async_sessionmaker, create_async_engine,
                                    AsyncSession)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


engine = create_async_engine(settings.async_database_url)

async_session_maker = async_sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    """Yield an asynchronous SQLAlchemy session for database operations.

    This function is intended to be used as a dependency in FastAPI routes
    to provide a database session that is properly managed and closed after
    use.
    """

    async with async_session_maker() as session:
        yield session


class Base(DeclarativeBase):
    """Base class for all ORM models in the application.

    All ORM models should inherit from this class to ensure they are
    registered with SQLAlchemy's metadata.
    """
