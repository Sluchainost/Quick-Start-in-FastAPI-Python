"""Service layer for ToDo business logic."""

from fastapi import HTTPException, status

from app.api.schemas.todo import ToDoCreate, ToDoFromDB, ToDoUpdate
from app.utils.unitofwork import IUnitOfWork


class ToDoService:
    """
    Service for ToDo operations.

    Handles business logic for ToDo CRUD operations.
    """

    def __init__(self, uow: IUnitOfWork):
        """
        Initialize the ToDoService with a Unit of Work.

        Args:
            uow (IUnitOfWork): The unit of work instance.
        """

        self.uow = uow

    async def add_todo(self, todo: ToDoCreate) -> ToDoFromDB:
        """
        Add a new ToDo item.

        Args:
            todo (ToDoCreate): The ToDo item to add.

        Returns:
            ToDoFromDB: The created ToDo item.
        """

        todo_dict: dict = todo.model_dump()

        try:
            async with self.uow:
                todo_from_db = await self.uow.todo.add_one(todo_dict)

                todo_to_return = ToDoFromDB.model_validate(todo_from_db)

                await self.uow.commit()

                return todo_to_return
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to add ToDo: {str(error)}"
                ) from error

    async def get_todo(self, todo_id: int) -> ToDoFromDB:
        """
        Retrieve a ToDo item by its ID.

        Args:
            todo_id (int): The ID of the ToDo item.

        Returns:
            ToDoFromDB: The retrieved ToDo item.
        """

        async with self.uow:
            todo = await self.uow.todo.find_one(todo_id)

            if not todo:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"ToDo item with ID {todo_id} not found"
                )

            return ToDoFromDB.model_validate(todo)

    async def update_todo(
                    self, todo_id: int, todo_data: ToDoUpdate) -> ToDoFromDB:
        """
        Update an existing ToDo item.

        Args:
            todo_id (int): The ID of the ToDo item.
            todo_data (ToDoUpdate): The data to update.

        Returns:
            ToDoFromDB: The updated ToDo item.
        """

        update_data = {k: v for k, v in todo_data.model_dump().items()
                       if v is not None}

        if not update_data:
            return await self.get_todo(todo_id)

        async with self.uow:
            existing_todo = await self.uow.todo.find_one(todo_id)

            if not existing_todo:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"ToDo item with ID {todo_id} not found)"
                )

            await self.uow.todo.update(todo_id, update_data)
            await self.uow.commit()

            refreshed_todo = await self.uow.todo.find_one(todo_id)
            return ToDoFromDB.model_validate(refreshed_todo)

    async def delete_todo(self, todo_id: int) -> dict:
        """
        Delete a ToDo item by its ID.

        Args:
            todo_id (int): The ID of the ToDo item.

        Returns:
            dict: A message indicating the result.
        """

        async with self.uow:
            existing_todo = await self.uow.todo.find_one(todo_id)

            if not existing_todo:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"ToDo item with ID {todo_id} not found"
                )

            deleted = await self.uow.todo.delete(todo_id)

            if deleted:
                await self.uow.todo.delete(todo_id)

                return {"message": "ToDo item successfully deleted"}

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to delete ToDo item"
            )
