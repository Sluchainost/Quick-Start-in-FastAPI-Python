"""This module sets up the SQLAlchemy ORM database connection and defines a custom declarative base class.

It provides:
- The SQLAlchemy engine and session for database operations.
- A custom Base class for ORM models, which includes common fields (id, created_at, updated_at).
- Automatic table name generation for derived models.

Intended for use as the foundation for all ORM models in the application.
"""

from datetime import datetime

from sqlalchemy import Integer, func, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    declared_attr,
    sessionmaker,
)

from step_5.lesson_5_3.task_5_3_15.config import settings


# Construct the database URL using application settings
DATABASE_URL = settings.get_db_url()

# Create the SQLAlchemy engine for database connectivity
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class and a session instance for ORM operations
Session = sessionmaker(bind=engine)
session = Session()


class Base(DeclarativeBase):
    """
    Custom declarative base class for all ORM models.

    This base class provides:
    - An auto-incrementing primary key 'id'
    - Timestamp fields 'created_at' and 'updated_at'
    - Automatic table name generation based on the class name

    All ORM models should inherit from this class.
    """

    __abstract__ = (
        True  # Mark as abstract base class (no table for Base itself)
    )

    # Primary key column (auto-incrementing integer)
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # Timestamp for when the record was created (set by the database)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),  # pylint: disable=not-callable
    )

    # Timestamp for when the record was last updated (auto-updated by the database)
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),  # pylint: disable=not-callable,
        onupdate=func.now(),  # pylint: disable=not-callable,
    )

    @classmethod
    @declared_attr.directive
    def __tablename__(cls) -> str:
        """
        Generate the table name for the ORM model.

        Returns:
            str: The table name, which is the lowercase class name with an 's' appended.
        """

        return cls.__name__.lower() + "s"
