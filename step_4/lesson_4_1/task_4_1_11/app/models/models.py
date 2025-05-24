""" User model definitions for the FastAPI authentication system.

This module contains Pydantic models used for data validation and serialization
in the authentication system.
"""

from pydantic import BaseModel


class User(BaseModel):
    """ Represents a user in the authentication system.

    Attributes:
        username (str): The unique identifier for the user
        password (str): The user's password
            (Note: In production, passwords should be hashed)
    """

    username: str
    password: str
