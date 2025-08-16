"""Tag Pydantic Schemas

This module defines Pydantic models (schemas) for Tag entities.
These schemas are used for data validation, serialization, and documentation in FastAPI endpoints.
Each schema serves a specific purpose in the CRUD lifecycle of a Tag.
"""

from pydantic import BaseModel, ConfigDict


class TagBase(BaseModel):
    """
    Base schema for Tag.

    This schema defines the common attributes shared by TagCreate, TagFromDB, and other tag-related schemas.
    It is not intended to be used directly for API requests or responses.
    """

    name: str  # The name of the tag (must be unique in the system).


class TagUpdate(BaseModel):
    """
    Schema for updating an existing Tag.

    This schema is used in update operations (PUT/PATCH requests).
    It allows partial or full updates of a tag's attributes.
    Currently, it is empty, but can be extended in the future if tag attributes become optional for updates.
    """

    # No fields are required for update at the moment.
    # Add optional fields here if partial updates are supported in the future.


class TagCreate(TagBase):
    """
    Schema for creating a new Tag.

    Inherits all required fields from TagBase.
    Used for validating the payload of POST requests when creating a new tag.
    """

    # Inherits 'name' from TagBase.


class TagFromDB(TagBase):
    """
    Schema representing a Tag as stored in the database.

    Extends TagBase by adding the unique identifier 'id'.
    Used for serializing Tag objects in API responses.
    """

    id: int  # Unique identifier of the tag in the database.

    # Pydantic configuration to allow ORM model instances to be parsed directly.
    model_config = ConfigDict(from_attributes=True)
