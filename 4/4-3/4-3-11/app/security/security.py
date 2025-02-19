"""JWT authentication and token management utilities.

This module provides functions for user authentication, JWT token generation,
and token validation. It uses PyJWT for token operations and integrates with
FastAPI's OAuth2 password flow.

Note:
    All JWT operations use the configured SECRET_KEY and ALGORITHM.
    Tokens include user role information for authorization.
"""

from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

import jwt

from security.pwdcrypt import verify_password
from models.models import User, Role, AuthUser
from db.db import get_user
from config import SECRET_KEY, ALGORITHM, EXPIRATION_TIME_SECONDS


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def authenticate_user(username: str, password: str) -> User | None:
    """Authenticate a user with username and password.

    Args:
        username (str): The username to authenticate.
        password (str): The password to verify.

    Returns:
        User | None: User object if authentication succeeds, None otherwise.
    """

    db_user = get_user(username)
    if db_user is None or not verify_password(password, db_user.password):
        return None
    return db_user


def get_exp() -> datetime:
    """Calculate token expiration time.

    Returns:
        datetime: UTC timestamp when the token will expire.
    """

    return (datetime.now(tz=timezone.utc) +
            timedelta(seconds=EXPIRATION_TIME_SECONDS))


def create_jwt_token(user: User) -> str:
    """Generate a JWT token for an authenticated user.

    Args:
        user (User): The user to create a token for.

    Returns:
        str: Encoded JWT token string.
    """

    data = {
        "sub": user.username,
        "role": user.role.name,
        "exp": get_exp()
    }
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def get_authuser_from_token(token: str = Depends(oauth2_scheme)) -> AuthUser:
    """Extract and validate user information from JWT token.

    Args:
        token (str): The JWT token to validate.

    Returns:
        AuthUser: Authenticated user information from token.

    Raises:
        HTTPException: 401 error if token is expired or invalid.
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM],)

        return AuthUser(
            username=payload.get("sub"),
            role=Role[payload.get("role")],
            )

    except jwt.ExpiredSignatureError as expired_signature_error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"}
        ) from expired_signature_error

    except jwt.InvalidTokenError as invalid_token_error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        ) from invalid_token_error
