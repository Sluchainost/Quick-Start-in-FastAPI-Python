"""This module defines the Pydantic schemas for ToDo operations.

It includes:
- ToDoCreate: Schema for creating a new ToDo item, specifying necessary fields.
- ToDoFromDB: Schema representing a ToDo item as returned
  from the database, extending ToDoCreate with additional fields.
"""

import datetime

from pydantic import BaseModel, ConfigDict


class ToDoCreate(BaseModel):
    """Schema for creating a new ToDo item.

    Attributes:
        description (str): A brief description of the to-do task.
        completed (bool, optional): Indicates if the task is completed.
    """

    description: str
    completed: bool | None = False


# we will return from the DB - inherited from creation and expanded by 2 fields
class ToDoFromDB(ToDoCreate):
    """Schema for representing a ToDo item from the database.

    This schema extends ToDoCreate by including additional fields that are
    set by the system such as the unique identifier and the creation timestamp.

    Attributes:
        id (int): Unique identifier for the ToDo item.
        created_at (datetime.datetime): Timestamp when the item was created.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime.datetime
