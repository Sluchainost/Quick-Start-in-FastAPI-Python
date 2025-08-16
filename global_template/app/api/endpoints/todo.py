"""ToDo API Endpoints

This module defines the FastAPI router for CRUD operations on ToDo items.
It provides endpoints for listing, retrieving, creating, updating, and deleting ToDos.
Each endpoint and dependency is thoroughly documented for clarity and educational purposes.
"""

from typing import List

from fastapi import APIRouter, Depends, status

from global_template.app.api.schemas.todo import (
    ToDoCreate,
    ToDoFromDB,
    ToDoUpdate,
)
from global_template.app.services.todo_service import ToDoService
from global_template.app.utils.unitofwork import (
    UnitOfWork,
    IUnitOfWork,
)
from global_template.app.db.database import async_session_maker


# Create an APIRouter instance for ToDo-related endpoints.
todo_router = APIRouter(prefix="/todos", tags=["ToDos"])


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


async def get_todo_service(
    uow: IUnitOfWork = Depends(get_uow),
) -> ToDoService:
    """
    Dependency provider for ToDoService.

    Args:
        uow: The UnitOfWork instance, injected by FastAPI's dependency system.

    Returns:
        An instance of ToDoService initialized with the provided UnitOfWork.

    This function allows endpoints to access business logic for ToDo operations.
    """

    return ToDoService(uow)


@todo_router.get("/", response_model=List[ToDoFromDB])
async def list_todos(todo_service: ToDoService = Depends(get_todo_service)):
    """
    Retrieve a list of all ToDo items.

    Args:
        todo_service: The ToDoService instance, injected by dependency.

    Returns:
        A list of ToDoFromDB objects representing all ToDos in the database.

    This endpoint allows clients to fetch all available ToDo items.
    """

    return await todo_service.get_all_todos()


@todo_router.get("/{todo_id}", response_model=ToDoFromDB)
async def get_todo(
    todo_id: int, todo_service: ToDoService = Depends(get_todo_service)
):
    """
    Retrieve a ToDo item by its unique ID.

    Args:
        todo_id: The unique identifier of the ToDo to retrieve.
        todo_service: The ToDoService instance, injected by dependency.

    Returns:
        A ToDoFromDB object representing the requested ToDo item.

    Raises:
        ToDoNotFoundError: If the ToDo with the specified ID does not exist.

    This endpoint allows clients to fetch a single ToDo by its ID.
    """

    return await todo_service.get_todo_by_id(todo_id)


@todo_router.post(
    "/", response_model=ToDoFromDB, status_code=status.HTTP_201_CREATED
)
async def create_todo(
    todo_create: ToDoCreate,
    todo_service: ToDoService = Depends(get_todo_service),
):
    """
    Create a new ToDo item.

    Args:
        todo_create: The data required to create a new ToDo (validated by ToDoCreate schema).
        todo_service: The ToDoService instance, injected by dependency.

    Returns:
        The newly created ToDoFromDB object.

    Raises:
        ToDoIntegrityError: If a ToDo with the same constraints already exists.
        HTTPException: For unexpected errors during ToDo creation.

    This endpoint allows clients to add a new ToDo item to the system.
    """

    return await todo_service.create_todo(todo_create)


@todo_router.put("/{todo_id}", response_model=ToDoFromDB)
async def update_todo(
    todo_id: int,
    todo_update: ToDoUpdate,
    todo_service: ToDoService = Depends(get_todo_service),
):
    """
    Update an existing ToDo item by its ID.

    Args:
        todo_id: The unique identifier of the ToDo to update.
        todo_update: The data to update (validated by ToDoUpdate schema).
        todo_service: The ToDoService instance, injected by dependency.

    Returns:
        The updated ToDoFromDB object.

    Raises:
        ToDoNotFoundError: If the ToDo with the specified ID does not exist.
        ToDoIntegrityError: If the update would violate database constraints.
        HTTPException: For unexpected errors during ToDo update.

    This endpoint allows clients to modify an existing ToDo item.
    """

    return await todo_service.update_todo(todo_id, todo_update)


@todo_router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: int, todo_service: ToDoService = Depends(get_todo_service)
):
    """
    Delete a ToDo item by its unique ID.

    Args:
        todo_id: The unique identifier of the ToDo to delete.
        todo_service: The ToDoService instance, injected by dependency.

    Returns:
        None. Returns HTTP 204 No Content on successful deletion.

    Raises:
        ToDoNotFoundError: If the ToDo with the specified ID does not exist.
        DBException: If the deletion fails due to a database error.

    This endpoint allows clients to remove a ToDo item from the system.
    """

    return await todo_service.delete_todo(todo_id)
