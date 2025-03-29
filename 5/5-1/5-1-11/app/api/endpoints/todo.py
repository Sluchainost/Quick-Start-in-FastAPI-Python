"""Module defining FastAPI endpoints for managing ToDo items.

This module provides RESTful endpoints for creating and retrieving
ToDo entries. It utilizes dependency injection to supply a ToDoService
instance through the Unit of Work pattern.
"""

from fastapi import APIRouter, Depends, status

from app.api.schemas.todo import ToDoCreate, ToDoFromDB, ToDoUpdate
from app.services.todo_service import ToDoService
from app.utils.unitofwork import UnitOfWork, IUnitOfWork


todo_router = APIRouter(
    prefix="/todo",
    tags=["ToDo"]
)


async def get_todo_service(
                            uow: IUnitOfWork = Depends(UnitOfWork)
                            ) -> ToDoService:
    """Dependency provider for ToDoService.

    This function uses FastAPI's dependency injection to create a
    Unit of Work (UOW) instance, which is then used to instantiate
    the ToDoService. This ensures that each request receives a fresh
    and properly managed database transaction context.

    Returns:
        ToDoService: An instance of the ToDoService configured with
                     a UOW dependency.
    """

    return ToDoService(uow)


@todo_router.get("/todos/", response_model=list[ToDoFromDB])
async def get_todos(todo_service: ToDoService = Depends(get_todo_service)):
    """Retrieve a list of all ToDo items.

    This endpoint fetches all ToDo entries from the database by delegating
    the retrieval operation to the ToDoService. All results are returned
    as a list of validated schemas.

    Args:
        todo_service (ToDoService): The service instance handling ToDo
                                    business logic.

    Returns:
        list[ToDoFromDB]: A list of ToDo items retrieved from the database.
    """

    return await todo_service.get_todos()


@todo_router.get("/todos/{todo_id}", response_model=ToDoFromDB)
async def get_todo(
                        todo_id: int,
                        todo_service: ToDoService = Depends(get_todo_service)
                        ):
    """Retrieve a single ToDo item by its ID.

    This endpoint fetches a specific ToDo entry from the database using its
    unique identifier. If the item is not found, an appropriate HTTP error
    response is returned.

    Args:
        todo_id (int): The unique identifier of the ToDo item to retrieve.
        todo_service (ToDoService): The service instance handling ToDo
                                    business logic.

    Returns:
        ToDoFromDB: The requested ToDo item if found.

    Raises:
        HTTPException: 404 error if the ToDo item is not found.
    """

    return await todo_service.get_todo_by_id(todo_id)


@todo_router.post("/todos/", response_model=ToDoFromDB,
                  status_code=status.HTTP_201_CREATED)
async def create_todo(
                        todo_data: ToDoCreate,
                        todo_service: ToDoService = Depends(get_todo_service)
                        ):
    """Create a new ToDo item.

    This endpoint accepts data for a new ToDo item, creates the database entry
    through the ToDoService, and returns the newly created ToDo item.
    The process ensures that the database transaction is handled atomically
    via the Unit of Work.

    Args:
        todo_data (ToDoCreate): The data payload for the new ToDo item.
        todo_service (ToDoService): The service instance managing ToDo
                                    creation logic.

    Returns:
        ToDoFromDB: The newly created ToDo item after being validated
                    against the schema.
    """

    return await todo_service.add_todo(todo_data)


@todo_router.put("/todos/{todo_id}", response_model=ToDoFromDB)
async def update_todo(
                        todo_id: int,
                        todo_data: ToDoUpdate,
                        todo_service: ToDoService = Depends(get_todo_service)
                        ):
    """Update an existing ToDo item

    This endpoint accepts data to update a specific ToDo item identified
    by its ID. It delegates the update operation to the ToDoService and returns
    the updated item. If the item is not found, an appropriate HTTP error
    response is returned.

    Args:
        todo_id (int): The unique identifier of the ToDo item to update.
        todo_data (ToDoUpdate): The data payload containing fields to update.
        todo_service (ToDoService): The service instance handling ToDo
                                    business logic.

    Returns:
        ToDoFromDB: The updated ToDo item after being validated against
                    the schema.

    Raises:
        HTTPException: 404 error if the ToDo item is not found.
    """

    return await todo_service.update_todo(todo_id, todo_data)


@todo_router.delete("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def delete_todo(
                        todo_id: int,
                        todo_service: ToDoService = Depends(get_todo_service)
                        ):
    """Delete a ToDo item.

    This endpoint deletes a specific ToDo item identified by its ID.
    It delegates the deletion operation to the ToDoServices and return
    a success message. If the item is not found, an appropriate HTTP
    error response is returned.

    Args:
        todo_id (int): The unique identifier of the ToDo item identified
                       by its ID.
        todo_service (ToDoService): The service instance handling ToDo
                                    business logic.

    Returns:
        dict: A message confirming successful deletion.

    Raises:
        HTTPException: 404 error if the ToDo item is not found.
    """

    return await todo_service.delete_todo(todo_id)
