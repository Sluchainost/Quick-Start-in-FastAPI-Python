"""Protected resource endpoints and access control.

This module provides FastAPI route handlers for protected resources with
role-based access control. It includes endpoints for admin, user, and
general access levels.

Note:
    All routes require valid JWT authentication.
    Role-specific endpoints verify appropriate access levels.
"""

from fastapi import APIRouter, Depends, HTTPException, status

from models.models import AuthUser, Role
from security.security import get_authuser_from_token


resource = APIRouter()


@resource.get("/admin/")
def get_admin_info(
    auth_user: AuthUser = Depends(get_authuser_from_token)
        ) -> dict:
    """Retrieve admin-only information.

    Args:
        auth_user (AuthUser): The authenticated user from JWT token.

    Returns:
        dict: A welcome message for admin users.

    Raises:
        HTTPException: 403 error if user is not an admin.
    """

    if auth_user.role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
            )

    return {"message": f"Hi admin {auth_user.username}!"}


@resource.get("/user/")
def get_user_info(
    auth_user: AuthUser = Depends(get_authuser_from_token)
        ) -> dict:
    """Retrieve user-level information.

    Args:
        auth_user (AuthUser): The authenticated user from JWT token.

    Returns:
        dict: A welcome message for standard users.

    Raises:
        HTTPException: 403 error if user lacks appropriate role.
    """

    if auth_user.role != Role.USER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
            )

    return {"message": f"Hi user {auth_user.username}!"}


@resource.get("/protected_resource/")
def get_protected_info(
    auth_user: AuthUser = Depends(get_authuser_from_token)
        ) -> dict:
    """Access protected resource available to both admin and users.

    Args:
        auth_user (AuthUser): The authenticated user from JWT token.

    Returns:
        dict: Welcome message and sensitive data for authorized users.

    Raises:
        HTTPException: 403 error if user lacks appropriate role.
    """

    if auth_user.role not in [Role.ADMIN, Role.USER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized"
            )

    return {"message": f"Hi user {auth_user.username}!",
            "data": "sensitive data"}


@resource.get("/info/")
def get_info(
    auth_user: AuthUser = Depends(get_authuser_from_token)
        ) -> dict:
    """Retrieve basic information available to all authenticated users.

    Args:
        auth_user (AuthUser): The authenticated user from JWT token.

    Returns:
        dict: A welcome message for any authenticated user.
    """

    return {"message": f"Hi {auth_user.username}!"}
