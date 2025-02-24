"""Database module for user management and authentication.

This module provides a simple in-memory database implementation for user
storage and retrieval. It includes predefined user accounts with different
role levels and functions to access user data.

Note:
    This is a simplified database implementation using dictionary storage.
    For production use, consider using a proper database system.

Attributes:
    USER_DATA (dict): A dictionary storing user information including
        username, encrypted password, and role assignments.
"""

from models.models import User, Role

from security.pwdcrypt import encode_password


USER_DATA = {}


USER_DATA["admin"] = {
                      "username": "admin",
                      "password": encode_password("admin"),
                      "role": Role.ADMIN
                      }

USER_DATA["user"] = {
                      "username": "user",
                      "password": encode_password("password"),
                      "role": Role.USER
                      }

USER_DATA["guest"] = {
                      "username": "guest",
                      "password": encode_password("12345"),
                      "role": Role.GUEST
                      }


def get_user(username: str) -> User | None:
    """Retrieve a user from the database by username.

    Args:
        username (str): The username to look up in the database.

    Returns:
        User | None: A User object if the username exists,
            None if the username is not found.

    Example:
        >>> user = get_user("admin")
        >>> if user:
        ...     print(user.username)
        'admin'
    """

    if username in USER_DATA:
        return User(**USER_DATA[username])
    return None
