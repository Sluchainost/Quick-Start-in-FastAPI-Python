"""Database models for the ToDo application.

This module defines ORM models using SQLAlchemy for the ToDo app.
"""

import datetime

from sqlalchemy import BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class ToDo(Base):
    """Represents a ToDo item in the database.

    Attributes:
        id (int): Unique identifier for the ToDo item.
        title (str): Title of the ToDo item.
        description (str): Detailed description of the ToDo item.
        completed (bool): Status indicating if the item is completed.
        created_at (datetime): Timestamp when the item was created.
    """

    __tablename__ = "todo"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    title: Mapped[str]
    description: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.datetime.now(datetime.timezone.utc)
    )
