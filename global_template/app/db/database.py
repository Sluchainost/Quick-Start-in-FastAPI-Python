"""Database setup module.

This module configures the asynchronous SQLAlchemy engine, sessionmaker,
and provides a declarative base class for ORM models with common fields.
It also defines a FastAPI dependency for obtaining an async database session.

Intended as a robust, educational template for scalable async database access.
"""

from datetime import datetime

import inflection

from sqlalchemy import Integer, func
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
    AsyncAttrs,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
    Mapped,
    mapped_column,
)

from global_template.app.core.config import settings


# -----------------------------------------------------------------------------
# Async Engine and Sessionmaker Setup
# -----------------------------------------------------------------------------

# Create an asynchronous SQLAlchemy engine using the database URL from settings.
# The 'echo' flag can be set to True for verbose SQL logging during development.
engine = create_async_engine(
    settings.async_database_url,
    echo=False,  # Set echo=True for SQL debug output
)

# Create an async sessionmaker factory that produces AsyncSession instances.
# 'expire_on_commit=False' prevents attributes from being expired after commit,
# which is generally preferred for async applications.
async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# -----------------------------------------------------------------------------
# FastAPI Dependency for Async Session
# -----------------------------------------------------------------------------


async def get_async_session():
    """
    FastAPI dependency that yields an asynchronous database session.

    Usage:
        Inject this dependency into FastAPI endpoints or services to
        perform database operations within a managed session context.

    Yields:
        AsyncSession: An active SQLAlchemy async session.
    """

    async with async_session_maker() as session:
        yield session


# -----------------------------------------------------------------------------
# Declarative Base Class for ORM Models
# -----------------------------------------------------------------------------


class Base(AsyncAttrs, DeclarativeBase):
    """
    Declarative base class for all ORM models.

    This base class provides:
      - Common fields: 'id', 'created_at', 'updated_at'
      - Automatic __tablename__ generation (plural, lowercase)
      - AsyncAttrs for compatibility with SQLAlchemy async ORM

    Attributes:
        id (int): Primary key, unique integer identifier for each record.
        created_at (datetime): Timestamp when the record was created.
        updated_at (datetime): Timestamp when the record was last updated.
    """

    __abstract__ = (
        True  # Prevents SQLAlchemy from creating a table for this base class.
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        doc="Primary key: unique integer identifier for each record.",
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),  # pylint: disable=not-callable
        doc="Timestamp when the record was created (set automatically by the database).",
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),  # pylint: disable=not-callable
        onupdate=func.now(),  # pylint: disable=not-callable
        doc="Timestamp when the record was last updated (set automatically by the database).",
    )

    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:  # pylint: disable=no-self-argument
        """
        Automatically generate the table name for the model.

        The table name is generated as the pluralized, lowercase form of the class name.
        For example, a class named 'UserProfile' becomes 'userprofiles'.

        Returns:
            str: The generated table name.
        """

        return inflection.pluralize(cls.__name__.lower())
