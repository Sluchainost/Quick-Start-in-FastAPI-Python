"""Database module for asynchronous sessions and model base configuration.

This module configures the asynchronous SQLAlchemy engine and session maker
using the application settings. It exposes an asynchronous session generator
for dependency injection in frameworks such as FastAPI, along with a base
class that models can inherit from.
"""

from sqlalchemy.ext.asyncio import (async_sessionmaker, create_async_engine,
                                    AsyncSession)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


# Create an asynchronous engine using the database URL from settings.
engine = create_async_engine(settings.async_database_url)

# Create an async sessionmaker that will generate AsyncSession instances.
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    """Asynchronous generator that yields a database session.

    This function is intended to be used as a dependency in framework routes,
    ensuring that each request gets a properly scoped asynchronous session.

    Yields:
        AsyncSession: An instance of SQLAlchemy's AsyncSession for
                      executing database operations.
    """

    async with async_session_maker() as session:
        yield session


class Base(DeclarativeBase):
    """Declarative base class for SQLAlchemy models.

    This class should be inherited by all model classes to ensure
    they are properly recognized by SQLAlchemy with the shared
    configuration defined here.
    """

    pass
