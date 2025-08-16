"""User Pydantic Schemas

This module defines Pydantic models (schemas) for User entities.
These schemas are used for data validation, serialization, and documentation in FastAPI endpoints.
Each schema serves a specific purpose in the CRUD lifecycle of a User.
Detailed docstrings and comments are provided for educational clarity.
"""

from typing import List, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    # Import only for type hints to avoid circular imports at runtime.
    from global_template.app.api.schemas.todo import ToDoFromDB


class UserBase(BaseModel):
    """
    Base schema for User.

    This schema defines the common attributes shared by UserCreate, UserFromDB, and other user-related schemas.
    It is not intended to be used directly for API requests or responses.
    """

    username: str  # The unique username of the user.
    email: str  # The user's email address.


class UserUpdate(BaseModel):
    """
    Schema for updating an existing User.

    This schema is used in update operations (PUT/PATCH requests).
    All fields are optional to allow partial updates.
    """

    username: str | None = None  # New username for the user (optional).
    email: str | None = None  # New email address for the user (optional).
    password: str | None = None  # New password for the user (optional).


class UserCreate(UserBase):
    """
    Schema for creating a new User.

    Inherits all required fields from UserBase and adds a password field.
    Used for validating the payload of POST requests when creating a new user.
    """

    password: str  # The password for the new user.


class UserFromDB(UserBase):
    """
    Schema representing a User as stored in the database.

    Extends UserBase by adding the unique identifier 'id' and a list of associated ToDo items.
    Used for serializing User objects in API responses.
    """

    id: int  # Unique identifier of the user in the database.
    todos: List["ToDoFromDB"] = (
        []
    )  # List of ToDo items associated with this user.

    # Pydantic configuration to allow ORM model instances to be parsed directly.
    model_config = ConfigDict(from_attributes=True)
