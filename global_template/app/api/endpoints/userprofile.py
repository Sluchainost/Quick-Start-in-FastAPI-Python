"""UserProfile API Endpoints

This module defines the FastAPI router for CRUD operations on user profiles.
It provides endpoints for listing, retrieving, creating, updating, and deleting user profiles.
All endpoints and dependencies are thoroughly documented for clarity and educational purposes.
"""

from typing import List

from fastapi import APIRouter, Depends, status

from global_template.app.api.schemas.userprofile import (
    UserProfileCreate,
    UserProfileFromDB,
    UserProfileUpdate,
)
from global_template.app.services.userprofile_service import (
    UserProfileService,
)
from global_template.app.utils.unitofwork import (
    UnitOfWork,
    IUnitOfWork,
)
from global_template.app.db.database import async_session_maker


# Create an APIRouter instance for user profile-related endpoints.
userprofile_router = APIRouter(prefix="/userprofiles", tags=["UserProfiles"])


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


async def get_userprofile_service(
    uow: IUnitOfWork = Depends(get_uow),
) -> UserProfileService:
    """
    Dependency provider for UserProfileService.

    Args:
        uow: The UnitOfWork instance, injected by FastAPI's dependency system.

    Returns:
        An instance of UserProfileService initialized with the provided UnitOfWork.

    This function allows endpoints to access business logic for user profile operations.
    """

    return UserProfileService(uow)


@userprofile_router.get("/", response_model=List[UserProfileFromDB])
async def list_userprofiles(
    userprofile_service: UserProfileService = Depends(get_userprofile_service),
):
    """
    Retrieve a list of all user profiles.

    Args:
        userprofile_service: The UserProfileService instance, injected by dependency.

    Returns:
        A list of UserProfileFromDB objects representing all user profiles in the database.

    This endpoint allows clients to fetch all available user profiles.
    """

    return await userprofile_service.get_all_profiles()


@userprofile_router.get("/{userprofile_id}", response_model=UserProfileFromDB)
async def get_userprofile(
    userprofile_id: int,
    userprofile_service: UserProfileService = Depends(get_userprofile_service),
):
    """
    Retrieve a user profile by its unique ID.

    Args:
        userprofile_id: The unique identifier of the user profile to retrieve.
        userprofile_service: The UserProfileService instance, injected by dependency.

    Returns:
        A UserProfileFromDB object representing the requested user profile.

    Raises:
        UserProfileNotFoundError: If the user profile with the specified ID does not exist.

    This endpoint allows clients to fetch a single user profile by its ID.
    """

    return await userprofile_service.get_profile_by_id(userprofile_id)


@userprofile_router.post(
    "/", response_model=UserProfileFromDB, status_code=status.HTTP_201_CREATED
)
async def create_userprofile(
    userprofile_create: UserProfileCreate,
    userprofile_service: UserProfileService = Depends(get_userprofile_service),
):
    """
    Create a new user profile.

    Args:
        userprofile_create: The data required to create a new user profile (validated by UserProfileCreate schema).
        userprofile_service: The UserProfileService instance, injected by dependency.

    Returns:
        The newly created UserProfileFromDB object.

    Raises:
        UserProfileIntegrityError: If a user profile with the same user_id already exists or violates constraints.
        HTTPException: For unexpected errors during user profile creation.

    This endpoint allows clients to add a new user profile to the system.
    """

    return await userprofile_service.create_profile(userprofile_create)


@userprofile_router.put("/{userprofile_id}", response_model=UserProfileFromDB)
async def update_userprofile(
    userprofile_id: int,
    userprofile_update: UserProfileUpdate,
    userprofile_service: UserProfileService = Depends(get_userprofile_service),
):
    """
    Update an existing user profile by its ID.

    Args:
        userprofile_id: The unique identifier of the user profile to update.
        userprofile_update: The data to update (validated by UserProfileUpdate schema).
        userprofile_service: The UserProfileService instance, injected by dependency.

    Returns:
        The updated UserProfileFromDB object.

    Raises:
        UserProfileNotFoundError: If the user profile with the specified ID does not exist.
        UserProfileIntegrityError: If the update would violate database constraints.
        HTTPException: For unexpected errors during user profile update.

    This endpoint allows clients to modify an existing user profile.
    """

    return await userprofile_service.update_profile(
        userprofile_id, userprofile_update
    )


@userprofile_router.delete(
    "/{userprofile_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_userprofile(
    userprofile_id: int,
    userprofile_service: UserProfileService = Depends(get_userprofile_service),
):
    """
    Delete a user profile by its unique ID.

    Args:
        userprofile_id: The unique identifier of the user profile to delete.
        userprofile_service: The UserProfileService instance, injected by dependency.

    Returns:
        None. Returns HTTP 204 No Content on successful deletion.

    Raises:
        UserProfileNotFoundError: If the user profile with the specified ID does not exist.
        DBException: If the deletion fails due to a database error.

    This endpoint allows clients to remove a user profile from the system.
    """

    return await userprofile_service.delete_profile(userprofile_id)
