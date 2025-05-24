"""
This module defines Pydantic schemas for data validation and serialization
of User and Profile entities in the scientific project.

Each schema is designed to facilitate robust data exchange between the API,
database models, and client applications, ensuring type safety and reproducibility.
"""

from typing import List

from pydantic import BaseModel, ConfigDict

from .sql_enums import GenderEnum, ProfessionEnum


class ProfilePydantic(BaseModel):
    """
    Pydantic schema for serializing and validating user profile data.

    Attributes:
        first_name (str): The user's first name (required).
        last_name (str | None): The user's last name (optional).
        age (int | None): The user's age (optional).
        gender (GenderEnum): The user's gender (enumerated, required).
        profession (ProfessionEnum): The user's profession (enumerated, required).
        interests (List[str] | None): List of user's interests (optional).
        contacts (dict | None): Arbitrary contact information (optional).
    """

    first_name: str
    last_name: str | None
    age: int | None
    gender: GenderEnum
    profession: ProfessionEnum
    interests: List[str] | None
    contacts: dict | None

    # Configures the schema to use attribute names from ORM models and serialize enums as values.
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class UserPydantic(BaseModel):
    """
    Pydantic schema for serializing and validating user account data.

    Attributes:
        username (str): Unique username for authentication.
        email (str): Unique email address.
        profile (ProfilePydantic | None): Nested profile data (optional).
    """

    username: str
    email: str
    profile: ProfilePydantic | None

    # Enables ORM mode and enum value serialization for compatibility with SQLAlchemy models.
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class UsernameIdPydantic(BaseModel):
    """
    Pydantic schema for serializing user ID and username pairs.

    Attributes:
        id (int): Unique user identifier.
        username (str): Unique username.
    """

    id: int
    username: str

    # Enables ORM mode for compatibility with SQLAlchemy models.
    model_config = ConfigDict(from_attributes=True)
