"""API endpoints for ToDo operations.

This module defines the FastAPI routes for creating, retrieving, updating,
and deleting ToDo items. It also provides dependency injection for the
ToDoService using a Unit of Work pattern.
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
    """ Dependency provider for ToDoService.

    Creates a ToDoService instance using the provided UnitOfWork.
    """

    return ToDoService(uow)


@todo_router.get("/todos/{todo_id}", response_model=ToDoFromDB)
async def get_todo(
                    todo_id: int,
                    todo_service: ToDoService = Depends(get_todo_service)
                    ):
    """ Retrieve a ToDo item by its ID.

    Args:
        todo_id (int): The ID of the ToDo item to retrieve.

    Returns:
        ToDoFromDB: The requested ToDo item.
    """

    return await todo_service.get_todo(todo_id)


@todo_router.post("/todos/", response_model=ToDoFromDB,
                  status_code=status.HTTP_201_CREATED)
async def create_todo(
                        todo_data: ToDoCreate,
                        todo_service: ToDoService = Depends(get_todo_service)
                        ):
    """ Create a new ToDo item.

    Args:
        todo_data (ToDoCreate): The data for the new ToDo item.

    Returns:
        ToDoFromDB: The created ToDo item.
    """

    return await todo_service.add_todo(todo_data)


@todo_router.put("/todos/{todo_id}", response_model=ToDoFromDB)
async def update_todo(
                        todo_id: int,
                        todo_data: ToDoUpdate,
                        todo_service: ToDoService = Depends(get_todo_service)
                        ):
    """ Update an existing ToDo item.

    Args:
        todo_id (int): The ID of the ToDo item to update.
        todo_data (ToDoUpdate): The updated data for the ToDo item.

    Returns:
        ToDoFromDB: The updated ToDo item.
    """

    return await todo_service.update_todo(todo_id, todo_data)


@todo_router.delete("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def delete_todo(
                        todo_id: int,
                        todo_service: ToDoService = Depends(get_todo_service)
                        ):
    """ Delete a ToDo item by its ID.

    Args:
        todo_id (int): The ID of the ToDo item to delete.

    Returns:
        dict: A message indicating the result of the deletion.
    """

    return await todo_service.delete_todo(todo_id)
