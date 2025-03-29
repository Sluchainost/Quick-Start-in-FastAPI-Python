"""Module for ToDo service operations.

This module provides the ToDoService class, which encapsulates the business
logic for managing ToDo items. It acts as an intermediary between the API
layer and the persistence layer, using the Unit of Work (UOW) pattern to
handle database transactions atomically.
"""

from fastapi import HTTPException, status

from app.api.schemas.todo import ToDoCreate, ToDoFromDB, ToDoUpdate
from app.utils.unitofwork import IUnitOfWork


class ToDoService:
    """Service class for ToDo operations.

    The ToDoService class provides methods to create and retrieve ToDo items.
    It leverages the Unit of Work (UOW) interface to ensure that operations
    involving database transactions are performed reliably and consistently.
    """

    def __init__(self, uow: IUnitOfWork):
        """Initialize the ToDoService.

        Args:
            uow (IUnitOfWork): An instance of a Unit of Work implementation
                               used for managing database transactions related
                               to ToDo operations.
        """

        self.uow = uow

    async def add_todo(self, todo: ToDoCreate) -> ToDoFromDB:
        """Add a new ToDo item.

        This method creates a new ToDo record in the database. It converts the
        input schema to a dictionary suitable for database insertion, adds the
        record within a transactional context, commits the transaction, and
        returns the newly created ToDo item as a validated schema object.

        Args:
            todo (ToDoCreate): Schema instance containing the ToDo details
                               for creation.

        Returns:
            ToDoFromDB: A validated schema instance representing the
                        newly created ToDo item.

        Raises:
            HTTPException: If any error occurs during the creation process.
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

    async def get_todos(self) -> list[ToDoFromDB]:
        """Retrieve all ToDo items.

        This method fetches all ToDo records from the database within a
        transactional context. It validates each record against the
        ToDoFromDB schema and returns the list of validated ToDo items.

        Returns:
            list[ToDoFromDB]: A list of validated schema instances
                              representing the ToDo items.

        Raises:
            HTTPException: If any error occurs during the retrieval process.
        """

        try:
            async with self.uow:
                todos: list = await self.uow.todo.find_all()

                return [ToDoFromDB.model_validate(todo) for todo in todos]
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch ToDos: {str(error)}"
            ) from error

    async def get_todo_by_id(self, todo_id: int) -> ToDoFromDB:
        """Retrieve a single ToDo item by its ID.

        This method fetches a single ToDo record from the database by its ID.
        if the record is not found, it raises an HTTPException with a
        404 status code.

        Args:
            todo_id (int): The unique identifier of the ToDo item to retrieve.

        Returns:
            ToDoFromDB: A validated schema instance representing the ToDo item.

        Raises:
            HTTPException: if the ToDo item with the specified ID is not found.
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
        """Update an existing ToDo item.

        This method updates a ToDo record in the database with the provided
        data. If the record is not found, it raises an HTTPException with
        a 404 status code.

        Args:
            todo_id (int): The unique identifier of the ToDo item to update.
            todo_data (ToDoUpdate): Schema instance containing the fields
                                    to update.

        Returns:
            ToDoFromDB: A validated schema instance representing the updated
                        ToDo item.

        Raises:
            HTTPException: If the ToDo item with the specified ID is not found.
        """

        update_data = {k: v for k, v in todo_data.model_dump().items()
                       if v is not None}

        if not update_data:
            # If no fields to update were provided,
            # just return the existing item
            return await self.get_todo_by_id(todo_id)

        async with self.uow:
            # First check if the todo exists
            existing_todo = await self.uow.todo.find_one(todo_id)

            if not existing_todo:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"ToDo item with ID {todo_id} not found"
                )

            # Update the todo
            await self.uow.todo.update(todo_id, update_data)
            await self.uow.commit()

            # Refresh the updated todo; ensures that all attributes
            # are correctly loaded for subsequent schema validation.
            refreshed_todo = await self.uow.todo.find_one(todo_id)
            return ToDoFromDB.model_validate(refreshed_todo)

    async def delete_todo(self, todo_id: int) -> dict:
        """Delete a ToDo item.

        This method deletes a ToDO record from the database by its ID.
        If the record is not found, it raises an HTTPException with
        a 404 status code.

        Args:
            todo_id (int): The unique identifier of the ToDo item to delete.

        Returns:
            dict: A dictionary containing a success message.

        Raises:
            HTTPException: If the ToDo item with the specified ID is not found.
        """

        async with self.uow:
            # Check if the todo exists before attempting deletion
            existing_todo = await self.uow.todo.find_one(todo_id)

            if not existing_todo:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"ToDo item with ID {todo_id} not found"
                )

            # Proceed to delete the item
            deleted = await self.uow.todo.delete(todo_id)

            if deleted:
                await self.uow.commit()

                return {"message": "ToDo item successfully deleted"}

            raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Failed to delete ToDo item"
                            )
