""" FastAPI application implementing basic HTTP authentication.

This module provides a simple REST API with basic authentication using username
and password credentials. It includes user verification against a mock database
and protected endpoint access.
"""

import uvicorn

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from models.models import User


app = FastAPI()
security = HTTPBasic()

USER_DATA = [User(**{"username": "user1", "password": "pass1"}),
             User(**{"username": "user2", "password": "pass2"})]


def get_user_from_db(username: str) -> str | None:
    """ Search for a user in the mock database by username.

    Args:
        username (str): The username to search for

    Returns:
        User | None: The User object if found, None otherwise
    """

    for user in USER_DATA:
        if user.username == username:
            return user

    return None


def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    """ Verify user credentials against the stored user data.

    Args:
        credentials (HTTPBasicCredentials):
            The credentials provided in the HTTP Basic Auth header

    Returns:
        User: The authenticated user object

    Raises:
        HTTPException: 401 status code if credentials are invalid
    """

    user = get_user_from_db(credentials.username)

    if user is None or user.password != credentials.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid credentials",
                            headers={"WWW-Authenticate": "Basic"},)

    return user


@app.get('/login/')
def get_protected_resource(user: User = Depends(authenticate_user)):
    """ Protected endpoint that requires valid authentication.

    Args:
        user (User): The authenticated user (injected by dependency)

    Returns:
        str: Welcome message including the authenticated username
    """

    return f'You got my secret, welcome {user.username}'


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
