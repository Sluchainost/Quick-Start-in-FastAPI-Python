"""Models for user authentication and role management.

This module defines the core data models used for user authentication, role
management, and request handling. It uses Pydantic for data validation and
Enum for role definitions.

Note:
    All models inherit from Pydantic's BaseModel for automatic validation
    and serialization support.
"""

from enum import Enum

from pydantic import BaseModel


class Role(Enum):
    """User role enumeration for access control.

    Defines the available user roles in the system, used for determining
    access levels and permissions.

    Attributes:
        ADMIN: Administrator role with full system access
        USER: Standard user role with normal privileges
        GUEST: Limited access role for unauthenticated users
    """

    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class AuthRequest(BaseModel):
    """Authentication request model.

    Data model for handling incoming authentication requests, containing
    the necessary credentials for user verification.

    Attributes:
        username (str): The user's login identifier
        password (str): The user's password in plain text
    """

    username: str
    password: str


class User(BaseModel):
    """User model containing full user information.

    Represents a complete user profile including authentication credentials
    and assigned role.

    Attributes:
        username (str): The user's unique identifier
        password (str): The user's hashed password
        role (Role): The user's assigned role in the system
    """

    username: str
    password: str
    role: Role


class AuthUser(BaseModel):
    """Authenticated user model for session management.

    Represents a user after successful authentication, containing only
    the necessary information for session handling.

    Attributes:
        username (str): The authenticated user's identifier
        role (Role): The user's role for permission checking
    """

    username: str
    role: Role
