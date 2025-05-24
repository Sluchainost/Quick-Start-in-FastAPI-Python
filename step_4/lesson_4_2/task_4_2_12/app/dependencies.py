"""JWT authentication module for token handling and user management."""

import datetime

import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from models.models import UserSchema

from database import USERS_DATA


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

TIME_NOW = datetime.datetime.now(datetime.UTC)
TOKEN_EXPIRATION_DATE_IN_MINUTES = 1


def get_user(username: str) -> UserSchema | None:
    """Retrieve user from database by username.

    Args:
        username (str): Username to search for.

    Returns:
        UserSchema | None: User object if found, None otherwise.
    """

    for user in USERS_DATA:
        if user.username == username:
            return user

    return None


def create_jwt_token(data: dict) -> str:
    """Generate JWT token with expiration time.

    Args:
        data (dict): Payload data for token generation.

    Returns:
        str: Encoded JWT token.
    """

    payload = data.copy()
    expiration_time = TIME_NOW + datetime.timedelta(
        minutes=TOKEN_EXPIRATION_DATE_IN_MINUTES
    )

    payload.update({'iat': TIME_NOW, 'exp': expiration_time})

    token = jwt.encode(
        payload=payload,
        key=SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


def get_user_from_token(token: str = Depends(oauth2_scheme)) -> str:
    """Extract and validate username from JWT token.

    Args:
        token (str): JWT token to decode.

    Returns:
        str: Username from token payload.

    Raises:
        HTTPException: When token is expired or invalid.
    """

    try:
        payload = jwt.decode(
            jwt=token,
            key=SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        username = payload.get("sub")

        return username

    except jwt.ExpiredSignatureError as expired_signature_error:
        raise HTTPException(
            detail='Access Token has expired or expiration date is invalid!',
            status_code=status.HTTP_401_UNAUTHORIZED
        ) from expired_signature_error
    except jwt.InvalidTokenError as invalid_token_error:
        raise HTTPException(
            detail='Invalid Token',
            status_code=status.HTTP_401_UNAUTHORIZED
        ) from invalid_token_error
