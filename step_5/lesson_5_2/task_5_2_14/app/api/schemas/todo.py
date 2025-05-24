"""Pydantic schemas for ToDo API requests and responses.

This module defines data models for creating, reading, and updating ToDo items.
"""

import datetime

from pydantic import BaseModel, ConfigDict


class ToDoCreate(BaseModel):
    """Schema for creating a new ToDo item.

    Attributes:
        title (str): The title of the ToDo item.
        description (str): The description of the ToDo item.
        completed (bool | None): Completion status, defaults to False.
    """

    title: str
    description: str
    completed: bool | None = False


class ToDoFromDB(ToDoCreate):
    """Schema for a ToDo item as stored in the database.

    Inherits all fields from ToDoCreate and adds:
        id (int): Unique identifier of the ToDo item.
        created_at (datetime): Timestamp when the item was created.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime.datetime


class ToDoUpdate(BaseModel):
    """Schema for updating an existing ToDo item.

    All fields are optional to allow partial updates.
    """

    title: str | None = None
    description: str | None = None
    completed: bool | None = None
