"""Database setup and base ORM model for SQLAlchemy with Alembic migration support.

This module configures the SQLAlchemy engine, session, and defines a reusable
declarative base class for ORM models. It is intended as an educational example
for learning about database migrations using Alembic.
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

from step_5.lesson_5_3.task_5_3_14.config import settings


# Obtain the database URL from the configuration settings.
DATABASE_URL = settings.get_db_url()

# Create the SQLAlchemy engine, which manages connections to the database.
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class and instantiate a session.
Session = sessionmaker(bind=engine)
session = Session()


class Base(DeclarativeBase):
    """
    Abstract base class for all ORM models.

    This class provides common columns and behaviors for all database tables,
    including:
      - An auto-incrementing primary key 'id'
      - Timestamp columns 'created_at' and 'updated_at'
      - Automatic table name generation based on the class name

    All ORM models should inherit from this class to ensure consistency and
    to simplify migration management with Alembic.
    """

    __abstract__ = (
        True  # Prevents SQLAlchemy from creating a table for this class.
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        doc="Primary key: unique identifier for each record.",
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),  # pylint: disable=not-callable
        doc="Timestamp when the record was created (set automatically).",
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),  # pylint: disable=not-callable,
        onupdate=func.now(),  # pylint: disable=not-callable,
        doc="Timestamp when the record was last updated (set automatically).",
    )

    @classmethod
    @declared_attr.directive
    def __tablename__(cls) -> str:
        """
        Automatically generate the table name for the ORM model.

        The table name is derived from the class name, converted to lowercase,
        and an 's' is appended (e.g., 'User' -> 'users').

        Returns:
            str: The generated table name.
        """

        return cls.__name__.lower() + "s"
