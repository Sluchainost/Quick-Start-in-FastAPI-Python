"""Password encryption and verification utilities.

This module provides functions for secure password hashing and verification
using bcrypt encryption scheme through passlib library.

Note:
    Uses CryptContext from passlib for consistent password hashing.
"""

from passlib.context import CryptContext


crypt_ctx = CryptContext(schemes=['bcrypt'])


def encode_password(password: str) -> str:
    """Hash a plain text password using bcrypt.

    Args:
        password (str): The plain text password to hash.

    Returns:
        str: The hashed password string.

    Example:
        >>> hashed = encode_password("mypassword123")
    """

    return crypt_ctx.hash(password)


def verify_password(password: str, encoded_password: str) -> bool:
    """Verify a password against its hashed version.

    Args:
        password (str): The plain text password to check.
        encoded_password (str): The hashed password to verify against.

    Returns:
        bool: True if password matches, False otherwise.

    Example:
        >>> is_valid = verify_password("mypassword123", hashed_password)
    """

    return crypt_ctx.verify(password, encoded_password)
