"""Data models for FastAPI application.

This module defines Pydantic models used for request validation
and data serialization/deserialization. Pydantic models provide
automatic data validation and parsing based on type annotations
and constraints.

Classes:
    User: Represents user data with validation constraints for each field.
"""

from typing import Optional
from pydantic import BaseModel, conint, EmailStr, constr


class User(BaseModel):
    """
    User data model for input validation.

    This model defines the expected structure and validation rules
    for user data submitted to the API. Pydantic will automatically
    validate incoming data against these constraints.

    Attributes:
        username (str): The user's name. Must be a non-empty string.
        age (int): The user's age. Must be an integer greater than 18.
        email (EmailStr): The user's email address. Must be a valid email format.
        password (str): The user's password. Must be 8-16 characters long.
        phone (Optional[str]): The user's phone number. Optional; defaults to 'Unknown'.
    """

    username: str
    age: conint(gt=18)  # type: ignore
    email: EmailStr
    password: constr(min_length=8, max_length=16)  # type: ignore
    phone: Optional[str] = "Unknown"
