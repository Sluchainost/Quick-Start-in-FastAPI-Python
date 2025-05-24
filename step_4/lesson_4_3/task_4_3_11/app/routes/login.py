"""Authentication routes and endpoints.

This module provides FastAPI route handlers for user authentication,
including login functionality and JWT token generation.

Note:
    All routes in this module are mounted under the auth router.
    Authentication failures raise appropriate HTTP exceptions.
"""

from fastapi import APIRouter, HTTPException, status

from models.models import AuthRequest, User
from security.security import authenticate_user, create_jwt_token


auth = APIRouter()


@auth.post("/login")
async def login(user: AuthRequest) -> dict:
    """Process user login requests and generate JWT tokens.

    Args:
        user (AuthRequest): The login request containing username and password.

    Returns:
        dict: A dictionary containing the JWT access token and token type.

    Raises:
        HTTPException: 401 error if credentials are invalid.

    Example:
        >>> response = await login(AuthRequest(username="user",
                                               password="pass"))
        >>> print(response)
        {'access_token': 'jwt_token_here', 'token_type': 'bearer'}
    """

    authenticated_user: User = authenticate_user(user.username, user.password)
    if authenticated_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
            )

    return {"access_token": create_jwt_token(authenticated_user),
            "token_type": "bearer"}
