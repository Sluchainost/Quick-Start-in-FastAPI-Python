"""Tag API Endpoints

This module defines the FastAPI router for CRUD operations on tags.
It provides endpoints for listing, retrieving, creating, updating, and deleting tags.
Each endpoint is documented for clarity and educational purposes.
"""

from typing import List

from fastapi import APIRouter, Depends, status


from global_template.app.api.schemas.tag import (
    TagCreate,
    TagFromDB,
    TagUpdate,
)
from global_template.app.services.tag_service import TagService
from global_template.app.utils.unitofwork import (
    UnitOfWork,
    IUnitOfWork,
)
from global_template.app.db.database import async_session_maker


# Create an APIRouter instance for tag-related endpoints.
tag_router = APIRouter(prefix="/tags", tags=["Tags"])


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


async def get_tag_service(
    uow: IUnitOfWork = Depends(get_uow),
) -> TagService:
    """
    Dependency provider for TagService.

    Args:
        uow: The UnitOfWork instance, injected by FastAPI's dependency system.

    Returns:
        An instance of TagService initialized with the provided UnitOfWork.

    This function allows endpoints to access business logic for tag operations.
    """

    return TagService(uow)


@tag_router.get("/", response_model=List[TagFromDB])
async def list_tags(tag_service: TagService = Depends(get_tag_service)):
    """
    Retrieve a list of all tags.

    Args:
        tag_service: The TagService instance, injected by dependency.

    Returns:
        A list of TagFromDB objects representing all tags in the database.

    This endpoint allows clients to fetch all available tags.
    """

    return await tag_service.get_all_tags()


@tag_router.get("/{tag_id}", response_model=TagFromDB)
async def get_tag(
    tag_id: int, tag_service: TagService = Depends(get_tag_service)
):
    """
    Retrieve a tag by its unique ID.

    Args:
        tag_id: The unique identifier of the tag to retrieve.
        tag_service: The TagService instance, injected by dependency.

    Returns:
        A TagFromDB object representing the requested tag.

    Raises:
        TagNotFoundError: If the tag with the specified ID does not exist.

    This endpoint allows clients to fetch a single tag by its ID.
    """

    return await tag_service.get_tag_by_id(tag_id)


@tag_router.post(
    "/", response_model=TagFromDB, status_code=status.HTTP_201_CREATED
)
async def create_tag(
    tag_create: TagCreate, tag_service: TagService = Depends(get_tag_service)
):
    """
    Create a new tag.

    Args:
        tag_create: The data required to create a new tag (validated by TagCreate schema).
        tag_service: The TagService instance, injected by dependency.

    Returns:
        The newly created TagFromDB object.

    Raises:
        TagIntegrityError: If a tag with the same name already exists.
        HTTPException: For unexpected errors during tag creation.

    This endpoint allows clients to add a new tag to the system.
    """

    return await tag_service.create_tag(tag_create)


@tag_router.put("/{tag_id}", response_model=TagFromDB)
async def update_tag(
    tag_id: int,
    tag_update: TagUpdate,
    tag_service: TagService = Depends(get_tag_service),
):
    """
    Update an existing tag by its ID.

    Args:
        tag_id: The unique identifier of the tag to update.
        tag_update: The data to update (validated by TagUpdate schema).
        tag_service: The TagService instance, injected by dependency.

    Returns:
        The updated TagFromDB object.

    Raises:
        TagNotFoundError: If the tag with the specified ID does not exist.
        TagIntegrityError: If the update would violate database constraints.
        HTTPException: For unexpected errors during tag update.

    This endpoint allows clients to modify an existing tag.
    """

    return await tag_service.update_tag(tag_id, tag_update)


@tag_router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(
    tag_id: int, tag_service: TagService = Depends(get_tag_service)
):
    """
    Delete a tag by its unique ID.

    Args:
        tag_id: The unique identifier of the tag to delete.
        tag_service: The TagService instance, injected by dependency.

    Returns:
        None. Returns HTTP 204 No Content on successful deletion.

    Raises:
        TagNotFoundError: If the tag with the specified ID does not exist.
        DBException: If the deletion fails due to a database error.

    This endpoint allows clients to remove a tag from the system.
    """

    return await tag_service.delete_tag(tag_id)
