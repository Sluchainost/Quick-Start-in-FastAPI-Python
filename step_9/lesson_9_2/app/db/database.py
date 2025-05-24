"""This module provides the configuration for the asynchronous database
   connection using SQLAlchemy's async engine.
It creates an asynchronous engine using database settings from the
configuration, configures an asynchronous sessionmaker, and supplies
a dependency generator for acquiring asynchronous database sessions.
Additionally, it defines a declarative base class for ORM model inheritance.
"""

from sqlalchemy.ext.asyncio import (async_sessionmaker, create_async_engine,
                                    AsyncSession)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


# Create the asynchronous engine using the configured database URL.
engine = create_async_engine(settings.async_database_url)

# Configure the session maker to create asynchronous sessions.
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    """Yield an asynchronous database session.

    This function is a dependency provider that yields a database session,
    ensuring that the session is properly closed after use. It is intended
    to be used with dependency injection in concurrency-safe operations.
    """

    async with async_session_maker() as session:
        yield session


class Base(DeclarativeBase):
    """Declarative base class for all ORM models.

    All ORM models should inherit from this base class to inherit the
    underlying mapping functionality provided by SQLAlchemy.
    This class centralizes metadata and configurations relevant to all models.
    """

    pass
