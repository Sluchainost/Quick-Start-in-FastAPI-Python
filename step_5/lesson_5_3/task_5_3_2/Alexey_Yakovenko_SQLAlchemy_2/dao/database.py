# pylint: disable=not-callable, no-self-argument

"""
This module provides the asynchronous SQLAlchemy database engine, session maker,
and a declarative base class for all ORM models in the project.

Key features:
- Asynchronous engine and session management for efficient DB operations.
- Custom base class with automatic table naming, timestamp fields, and dictionary serialization.
- Annotated type aliases for common column patterns.
"""

from typing import Annotated, List

from datetime import datetime

from sqlalchemy import Integer, String, ARRAY, Text, func
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
    Mapped,
    mapped_column,
    class_mapper,
)
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    async_sessionmaker,
    create_async_engine,
)

from ..config import settings


# Retrieve the database URL from the project settings.
DATABASE_URL = settings.get_db_url()

# Create an asynchronous SQLAlchemy engine.
engine = create_async_engine(url=DATABASE_URL)

# Create an asynchronous session maker.
# Setting expire_on_commit=False prevents SQLAlchemy from expiring objects after commit,
# which is often desirable in async workflows.
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

# Type aliases for commonly used column patterns in the project.
uniq_str_an = Annotated[
    str, mapped_column(unique=True)
]  # Unique string column
array_or_none_an = Annotated[
    List[str] | None, mapped_column(ARRAY(String))
]  # Optional array of strings
content_an = Annotated[str, Mapped[Text]]  # Text content column


class Base(AsyncAttrs, DeclarativeBase):
    """
    Abstract base class for all ORM models in the project.

    Features:
    - Provides an auto-incrementing primary key 'id'.
    - Automatically adds 'created_at' and 'updated_at' timestamp fields.
    - Dynamically generates table names based on class names.
    - Includes a utility method for serializing model instances to dictionaries.
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
        server_default=func.now(),
        doc="Timestamp when the record was created (set automatically by the database).",
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        doc="Timestamp when the record was last updated (set automatically by the database).",
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """
        Automatically generates the table name for the model.

        Returns:
            str: Table name, which is the lowercase class name with an 's' appended.
                 For example, 'User' becomes 'users'.
        """

        return cls.__name__.lower() + "s"

    def to_dict(self) -> dict:
        """
        Serializes the model instance to a dictionary, including all column fields.

        Returns:
            dict: A dictionary mapping column names to their values for this instance.
        """

        columns = class_mapper(self.__class__).columns

        # Extract all column values into a dictionary for easy serialization.
        return {column.key: getattr(self, column.key) for column in columns}
