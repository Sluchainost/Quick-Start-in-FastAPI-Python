"""ToDo Pydantic Schemas

This module defines Pydantic models (schemas) for ToDo entities.
These schemas are used for data validation, serialization, and documentation in FastAPI endpoints.
Each schema serves a specific purpose in the CRUD lifecycle of a ToDo item.
Detailed docstrings and comments are provided for educational clarity.
"""

import datetime

from typing import List, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    # These imports are only used for type hints to avoid circular imports at runtime.
    from global_template.app.api.schemas.tag import TagFromDB
    from global_template.app.api.schemas.user import UserFromDB


class ToDoBase(BaseModel):
    """
    Base schema for ToDo items.

    This schema defines the common attributes shared by ToDoCreate, ToDoFromDB, and other ToDo-related schemas.
    It is not intended to be used directly for API requests or responses.
    """

    title: str  # The title of the ToDo item.
    description: str | None = (
        None  # Optional detailed description of the ToDo.
    )
    completed: bool = False  # Completion status of the ToDo (default: False).


class ToDoUpdate(BaseModel):
    """
    Schema for updating an existing ToDo item.

    This schema is used in update operations (PUT/PATCH requests).
    All fields are optional to allow partial updates.
    """

    title: str | None = None  # New title for the ToDo (optional).
    description: str | None = None  # New description for the ToDo (optional).
    completed: bool | None = None  # New completion status (optional).
    user_id: int | None = None  # Optionally reassign ToDo to a different user.
    tag_ids: List[int] | None = None  # Optionally update associated tags.


class ToDoCreate(ToDoBase):
    """
    Schema for creating a new ToDo item.

    Inherits all required fields from ToDoBase and adds user and tag associations.
    Used for validating the payload of POST requests when creating a new ToDo.
    """

    user_id: int  # The ID of the user to whom this ToDo belongs.
    tag_ids: List[int] | None = (
        []
    )  # Optional list of tag IDs to associate with the ToDo.


class ToDoFromDB(ToDoBase):
    """
    Schema representing a ToDo item as stored in the database.

    Extends ToDoBase by adding the unique identifier 'id', creation timestamp,
    and relationships to user and tags. Used for serializing ToDo objects in API responses.
    """

    id: int  # Unique identifier of the ToDo in the database.
    created_at: datetime.datetime  # Timestamp when the ToDo was created.
    user: "UserFromDB"  # The user to whom this ToDo belongs.
    tags: List["TagFromDB"] = []  # List of tags associated with this ToDo.

    # Pydantic configuration to allow ORM model instances to be parsed directly.
    model_config = ConfigDict(from_attributes=True)
