"""Module for ORM models used across the application.

This module defines database models that structure the data used throughout
the system. Each model is based on the common SQLAlchemy configuration
inherited from the base class.
"""

import datetime

from sqlalchemy import BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class ToDo(Base):
    """Model for representing a to-do item.

    Attributes:
        id (int): Unique identifier for each to-do item.
        title (str): The title of the to-do item.
        description (str): A short description of the task to be completed.
        completed (bool): Status flag indicating whether the task is completed;
                          defaults to False.
        create_at (datetime.datetime): Timestamp marking when the to-do item
                                       was created. It automatically captures
                                       the current UTC time.
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
