"""Service layer for managing ToDo items.

This module provides a service class that encapsulates business logic for
creating and retrieving ToDo items. It interacts with a Unit of Work instance
to coordinate database operations and ensure transactional consistency.
"""

from app.api.schemas.todo import ToDoCreate, ToDoFromDB
from app.utils.unitofwork import IUnitOfWork


class ToDoService:
    """Service class for handling ToDo operations.

    This class provides methods to add a new ToDo item and retrieve existing
    ToDo items from the database using the provided Unit of Work. It handles
    data preparation, transaction management, and transformation of data
    between API schemas and database models.
    """

    def __init__(self, uow: IUnitOfWork):
        """Initialize the ToDoService with a Unit of Work.

        Args:
            uow (IUnitOfWork): An instance implementing the Unit of Work
                               interface, responsible for managing database
                               transactions and repositories.
        """

        self.uow = uow

    async def add_todo(self, todo: ToDoCreate) -> ToDoFromDB:
        """Add a new ToDo item to the database.

        This method prepares the ToDo item data for insertion, uses the
        Unit of Work to add the item through the repository, validates
        the returned database model, and commits the transaction. If any
        error occurs during the transaction, all changes will be rolled back.

        Args:
            todo (ToDoCreate): Data model containing information for creating
                               a new ToDo item.

        Returns:
            ToDoFromDB: A validated ToDo item model representing the newly
                        added record in the database.
        """

        # preparing data for entering into the database
        todo_dict: dict = todo.model_dump()

        # enter the context (if it exits with an error,
        # the changes will be rolled back)
        async with self.uow:
            todo_from_db = await self.uow.todo.add_one(todo_dict)

            # processing the received data from the DB to return it
            # making a pedantic model
            todo_to_return = ToDoFromDB.model_validate(todo_from_db)

            # this is the most important piece of code, before this
            # commit you can write data to 50 models, but if someone
            # crashes with an error, all changes will be rolled back!
            # If the code got here, then everything went ok!
            await self.uow.commit()

            return todo_to_return

    async def get_todos(self) -> list[ToDoFromDB]:
        """Retrieve all ToDo items from the database.

        This method fetches all ToDo records using the Unit of Work's
        repository, validates each record against the ToDoFromDB model,
        and returns them as a list.

        Returns:
            list[ToDoFromDB]: A list of validated ToDo item models retrieved
                              from the database.
        """

        async with self.uow:
            todos: list = await self.uow.todo.find_all()

            return [ToDoFromDB.model_validate(todo) for todo in todos]
