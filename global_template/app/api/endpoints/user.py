"""User API Endpoints

This module defines the FastAPI router for CRUD operations on users.
It provides endpoints for listing, retrieving, creating, updating, and deleting users.
All endpoints and dependencies are thoroughly documented for clarity and educational purposes.
"""

from typing import List

from fastapi import APIRouter, Depends, status

from global_template.app.api.schemas.user import (
    UserCreate,
    UserFromDB,
    UserUpdate,
)
from global_template.app.services.user_service import UserService
from global_template.app.utils.unitofwork import (
    UnitOfWork,
    IUnitOfWork,
)
from global_template.app.db.database import async_session_maker


# Create an APIRouter instance for user-related endpoints.
user_router = APIRouter(prefix="/users", tags=["Users"])


async def get_uow() -> IUnitOfWork:
    """
    Dependency provider for the UnitOfWork.

    Returns:
        An instance of UnitOfWork configured with the async session maker.

    This function is used as a dependency in endpoints to ensure that
    each request gets its own UnitOfWork instance, managing database
    transactions and repository access.
    """

    return UnitOfWork(async_session_maker)


async def get_user_service(
    uow: IUnitOfWork = Depends(get_uow),
) -> UserService:
    """
    Dependency provider for UserService.

    Args:
        uow: The UnitOfWork instance, injected by FastAPI's dependency system.

    Returns:
        An instance of UserService initialized with the provided UnitOfWork.

    This function allows endpoints to access business logic for user operations.
    """

    return UserService(uow)


@user_router.get("/", response_model=List[UserFromDB])
async def list_users(user_service: UserService = Depends(get_user_service)):
    """
    Retrieve a list of all users.

    Args:
        user_service: The UserService instance, injected by dependency.

    Returns:
        A list of UserFromDB objects representing all users in the database.

    This endpoint allows clients to fetch all registered users.
    """

    return await user_service.get_all_users()


@user_router.get("/{user_id}", response_model=UserFromDB)
async def get_user(
    user_id: int, user_service: UserService = Depends(get_user_service)
):
    """
    Retrieve a user by their unique ID.

    Args:
        user_id: The unique identifier of the user to retrieve.
        user_service: The UserService instance, injected by dependency.

    Returns:
        A UserFromDB object representing the requested user.

    Raises:
        UserNotFoundError: If the user with the specified ID does not exist.

    This endpoint allows clients to fetch a single user by their ID.
    """

    return await user_service.get_user_by_id(user_id)


@user_router.post(
    "/", response_model=UserFromDB, status_code=status.HTTP_201_CREATED
)
async def create_user(
    user_create: UserCreate,
    user_service: UserService = Depends(get_user_service),
):
    """
    Create a new user.

    Args:
        user_create: The data required to create a new user (validated by UserCreate schema).
        user_service: The UserService instance, injected by dependency.

    Returns:
        The newly created UserFromDB object.

    Raises:
        UserAlreadyExistsError: If a user with the same email already exists.
        UserIntegrityError: If a database integrity error occurs.
        HTTPException: For unexpected errors during user creation.

    This endpoint allows clients to register a new user in the system.
    """

    return await user_service.create_user(user_create)


@user_router.put("/{user_id}", response_model=UserFromDB)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    user_service: UserService = Depends(get_user_service),
):
    """
    Update an existing user by their ID.

    Args:
        user_id: The unique identifier of the user to update.
        user_update: The data to update (validated by UserUpdate schema).
        user_service: The UserService instance, injected by dependency.

    Returns:
        The updated UserFromDB object.

    Raises:
        UserNotFoundError: If the user with the specified ID does not exist.
        UserIntegrityError: If the update would violate database constraints.
        HTTPException: For unexpected errors during user update.

    This endpoint allows clients to modify an existing user's information.
    """

    return await user_service.update_user(user_id, user_update)


@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int, user_service: UserService = Depends(get_user_service)
):
    """
    Delete a user by their unique ID.

    Args:
        user_id: The unique identifier of the user to delete.
        user_service: The UserService instance, injected by dependency.

    Returns:
        None. Returns HTTP 204 No Content on successful deletion.

    Raises:
        UserNotFoundError: If the user with the specified ID does not exist.
        DBException: If the deletion fails due to a database error.

    This endpoint allows clients to remove a user from the system.
    """

    return await user_service.delete_user(user_id)
