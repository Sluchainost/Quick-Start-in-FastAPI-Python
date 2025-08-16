"""DOC"""

from fastapi import HTTPException, status

from sqlalchemy.exc import IntegrityError

from global_template.app.api.schemas.todo import (
    ToDoCreate,
    ToDoFromDB,
    ToDoUpdate,
)
from global_template.app.utils.unitofwork import IUnitOfWork
from global_template.app.exceptions.todo_exceptions import (
    ToDoNotFoundError,
    ToDoIntegrityError,
)
from global_template.app.exceptions.db_exceptions import (
    DBException,
)


class ToDoService:
    """DOC"""

    def __init__(self, uow: IUnitOfWork):
        """DOC"""

        self.uow = uow

    async def create_todo(self, todo_create: ToDoCreate) -> ToDoFromDB:
        """DOC"""

        todo_data: dict = todo_create.model_dump()

        try:
            async with self.uow:
                todo_db = await self.uow.todo.add_one(todo_data)

                await self.uow.commit()

                return ToDoFromDB.model_validate(todo_db)
        except IntegrityError as e:
            raise ToDoIntegrityError(
                message_key="todo.create.integrity_error",
                message_params={"user_id": todo_data.get("user_id")},
            ) from e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create todo: {e}",
            ) from e

    async def get_all_todos(self) -> list[ToDoFromDB]:
        """DOC"""

        async with self.uow:
            todos = await self.uow.todo.get_all()

            return [ToDoFromDB.model_validate(t) for t in todos]

    async def get_todo_by_id(self, todo_id: int) -> ToDoFromDB:
        """DOC"""

        async with self.uow:
            todo = await self.uow.todo.get_by_id(todo_id)

            if not todo:
                raise ToDoNotFoundError(message_params={"todo_id": todo_id})

            return ToDoFromDB.model_validate(todo)

    async def update_todo(
        self, todo_id: int, todo_update: ToDoUpdate
    ) -> ToDoFromDB:
        """DOC"""

        update_data = {
            k: v for k, v in todo_update.model_dump().items() if v is not None
        }

        if not update_data:
            return await self.get_todo_by_id(todo_id)

        try:
            async with self.uow:
                todo = await self.uow.todo.get_by_id(todo_id)

                if not todo:
                    raise ToDoNotFoundError(
                        message_params={"todo_id": todo_id}
                    )

                await self.uow.todo.update(todo_id, update_data)
                await self.uow.commit()

                todo = await self.uow.todo.get_by_id(todo_id)

                return ToDoFromDB.model_validate(todo)
        except IntegrityError as e:
            raise ToDoIntegrityError(
                message_key="todo.update.integrity_error",
                message_params={"todo_id": todo_id},
            ) from e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update todo: {e}",
            ) from e

    async def delete_todo(self, todo_id: int) -> None:
        """DOC"""

        async with self.uow:
            todo = await self.uow.todo.get_by_id(todo_id)

            if not todo:
                raise ToDoNotFoundError(message_params={"todo_id": todo_id})

            deleted = await self.uow.todo.delete(todo_id)

            if not deleted:
                raise DBException(message_key="errors.todo.delete_failed")

            await self.uow.commit()
