"""Module for implementing the Unit of Work pattern for managing database
   transactions.

This module defines an abstract base interface (IUnitOfWork) and a concrete
implementation (UnitOfWork) that provide a structured approach to managing
asynchronous database sessions and transactions. Using this pattern ensures
that operations performed on repositories, such as the ToDoRepository, are
executed atomically. In case of errors, transactions are properly rolled back
to maintain data consistency.
"""

from abc import ABC, abstractmethod

from app.db.database import async_session_maker
from app.repositories.todo_repository import ToDoRepository


class IUnitOfWork(ABC):
    """Abstract interface for Unit of Work patterns in asynchronous operations.

    This interface enforces the implementation of context management, commit,
    and rollback methods across concrete Unit of Work implementations.
    These methods ensure proper handling of database transactions.
    """

    todo: ToDoRepository

    @abstractmethod
    def __init__(self):
        """Initialize the Unit of Work interface.

        Sets up any necessary configuration before entering the
        transactional context.
        """

    @abstractmethod
    async def __aenter__(self):
        """Enter the async context.

        Prepares the database session and repository instances
        (e.g., ToDoRepository) for transactional operations.
        Returns:
            An instance of the Unit of Work ready to perform operations.
        """

    @abstractmethod
    async def __aexit__(self, *args):
        """Exit the async context.

        Handles cleanup by rolling back any pending transactions and closing
        the database session.
        Args:
            *args: Exception details if an error has occurred.
        """

    @abstractmethod
    async def commit(self):
        """Commit the current transaction.

        Persists all changes made during the Unit of Work session
        to the database.
        Raises:
            Exception: Propagates exceptions raised during the
            commit operation.
        """

    @abstractmethod
    async def rollback(self):
        """Rollback the current transaction.

        Reverts all changes made during the Unit of Work session in case
        of errors or cancellations.
        """


class UnitOfWork(IUnitOfWork):
    """Concrete implementation of the asynchronous Unit of Work pattern.

    Manages the lifecycle of the database session and provides repository
    access (e.g., ToDoRepository) to ensure that all operations within
    the context are executed within a single transaction.
    """

    def __init__(self):
        """Initialize the UnitOfWork instance.

        Sets the asynchronous session factory for creating new
        database sessions.
        """

        self.session_factory = async_session_maker
        self.session = self.session_factory()

    async def __aenter__(self):
        """Enter the asynchronous context.

        Creates a new database session and instantiates the ToDo repository
        with the session for transactional operations.
        Returns:
            The UnitOfWork instance with an active session and repository set.
        """

        self.todo = ToDoRepository(self.session)

    async def __aexit__(self, *args):
        """Exit the asynchronous context.

        Rolls back any pending transactions and closes the database session
        to ensure resource cleanup.
        Args:
            *args: Exception details if any error occurs during the context.
        """

        await self.rollback()
        await self.session.close()

    async def commit(self):
        """Commit the transaction.

        Persists all changes made during the session to the database.
        """

        await self.session.commit()

    async def rollback(self):
        """Rollback the transaction.

        Undoes all uncommitted changes made during the session to
        maintain data consistency.
        """

        await self.session.rollback()
