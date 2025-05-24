""" ToDo API Endpoints

This module defines the API endpoints for managing ToDo items.
Endpoints include retrieving a list of todo items and creating a new todo item.
"""

from fastapi import APIRouter, Depends

from app.api.schemas.todo import ToDoCreate, ToDoFromDB
from app.services.todo_service import ToDoService
from app.utils.unitofwork import UnitOfWork, IUnitOfWork


todo_router = APIRouter(
    prefix="/todo",
    tags=["ToDo"]
)


async def get_todo_service(
                            uow: IUnitOfWork = Depends(UnitOfWork)
                           ) -> ToDoService:
    """
    Dependency provider for the ToDoService.

    Uses dependency injection to supply a UnitOfWork instance (via IUnitOfWork)
    to instantiate and return a ToDoService, ensuring transactional control.
    """

    return ToDoService(uow)


@todo_router.get("/todos/", response_model=list[ToDoFromDB])
async def get_todos(todo_service: ToDoService = Depends(get_todo_service)):
    """
    Retrieve all ToDo items.

    This endpoint returns a list of ToDo items,
    each represented by the ToDoFromDB schema.
    It leverages the ToDoService to interact with the datastore.
    """

    return await todo_service.get_todos()


@todo_router.post("/todos/", response_model=ToDoFromDB)
async def create_todo(
                       todo_data: ToDoCreate,
                       todo_service: ToDoService = Depends(get_todo_service)
                       ):
    """
    Create a new ToDo item.

    Accepts a ToDoCreate payload to create a new ToDo entry in the datastore.
    Returns the created ToDo item using the ToDoFromDB schema
    from the database after the commit.
    """

    return await todo_service.add_todo(todo_data)
