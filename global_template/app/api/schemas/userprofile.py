"""UserProfile Pydantic Schemas

This module defines Pydantic models (schemas) for UserProfile entities.
These schemas are used for data validation, serialization, and documentation in FastAPI endpoints.
Each schema serves a specific purpose in the CRUD lifecycle of a UserProfile.
Detailed docstrings and comments are provided for educational clarity.
"""

from pydantic import BaseModel, ConfigDict


class UserProfileBase(BaseModel):
    """
    Base schema for UserProfile.

    This schema defines the common attributes shared by UserProfileCreate, UserProfileFromDB, and other user profile-related schemas.
    It is not intended to be used directly for API requests or responses.
    """

    bio: str  # A short biography or description for the user.
    avatar_url: str  # URL to the user's avatar image.


class UserProfileUpdate(BaseModel):
    """
    Schema for updating an existing UserProfile.

    This schema is used in update operations (PUT/PATCH requests).
    All fields are optional to allow partial updates.
    """

    bio: str | None = None  # New biography for the user (optional).
    avatar_url: str | None = None  # New avatar URL for the user (optional).


class UserProfileCreate(UserProfileBase):
    """
    Schema for creating a new UserProfile.

    Inherits all required fields from UserProfileBase and adds a user_id field.
    Used for validating the payload of POST requests when creating a new user profile.
    """

    user_id: int  # The ID of the user to whom this profile belongs.


class UserProfileFromDB(UserProfileBase):
    """
    Schema representing a UserProfile as stored in the database.

    Extends UserProfileBase by adding the unique identifier 'id' and the associated 'user_id'.
    Used for serializing UserProfile objects in API responses.
    """

    id: int  # Unique identifier of the user profile in the database.
    user_id: int  # The ID of the user to whom this profile belongs.

    # Pydantic configuration to allow ORM model instances to be parsed directly.
    model_config = ConfigDict(from_attributes=True)
