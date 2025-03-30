"""Schemas for ToDo API

This module defines the data models for creating and retrieving ToDo items.

Classes:
    ToDoCreate: Schema for creating a new ToDo item.
    ToDoFromDB: Schema representing a ToDo item as stored in the database.
    ToDoUpdate: Schema for updating an existing ToDo item.
"""

import datetime

from pydantic import BaseModel, ConfigDict


class ToDoCreate(BaseModel):
    """Schema for creating a new ToDo item.

    Attributes:
        title (str): The title of the ToDo item.
        description (str): The description or text content of the ToDo item.
        completed (bool, optional): Indicator if the ToDo is completed.
                                    Defaults to False.
    """

    title: str
    description: str
    completed: bool | None = False


class ToDoFromDB(ToDoCreate):
    """Schema representation of a ToDo item retrieved from the database.

    Inherits from ToDoCreate and adds database-specific fields.

    Attributes:
        id: Unique identifier for the ToDo item.
        created_at: Timestamp when the ToDo item was created.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime.datetime


class ToDoUpdate(BaseModel):
    """Schema for updating an existing ToDo item.

    Attributes:
        title (str, optional): The updates title of the ToDo item.
        description (str, optional): The updated description of the ToDo item.
        completed (bool, optional): The updated completion status.
    """

    title: str | None = None
    description: str | None = None
    completed: bool | None = None
