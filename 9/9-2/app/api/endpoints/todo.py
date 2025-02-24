""" DOC """

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.todo import ToDoCreate, ToDoFromDB
from app.db.database import get_async_session
from app.repositories.todo_repository import (ToDoRepository,
                                              SqlAlchemyToDoRepository)


todo_router = APIRouter(
    prefix="/todo",
    tags=["ToDo"]
)


async def get_todo_repository(
                        session: AsyncSession = Depends(get_async_session)
                             ) -> ToDoRepository:
    """ DOC """

    return SqlAlchemyToDoRepository(session)


@todo_router.get("/", response_model=list[ToDoFromDB])
async def get_todos(repo: ToDoRepository = Depends(get_todo_repository)):
    """ DOC """

    return await repo.get_todos()


@todo_router.post("/", response_model=ToDoFromDB)
async def create_todos(
                       todo: ToDoCreate,
                       repo: ToDoRepository = Depends(get_todo_repository)
                       ):
    """ DOC """

    return await repo.create_todo(todo)
