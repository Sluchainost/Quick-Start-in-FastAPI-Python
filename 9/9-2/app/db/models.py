"""This module defines the ORM model for ToDo items using SQLAlchemy.
It contains the ToDo model that maps to the "todo" table in the database.
"""

import datetime

from sqlalchemy import BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class ToDo(Base):
    """Represents a ToDo item in the database.

    Attributes:
        id (int): Unique identifier of the ToDo item.
        description (str): Textual description of the ToDo item.
        completed (bool): Indicates whether the ToDo item is completed.
        created_at (datetime.datetime): Timestamp when the item was created.
    """

    __tablename__ = "todo"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    description: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
                                                DateTime,
                                                nullable=False,
                                                default=datetime.UTC
                                                    )
