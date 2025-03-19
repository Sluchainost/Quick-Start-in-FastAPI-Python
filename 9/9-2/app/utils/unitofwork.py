"""Unit of Work Pattern Implementation

This module defines the interface and concrete implementation for the
Unit of Work pattern, ensuring that a series of operations can be treated
as a single transactional unit. It is designed to work with asynchronous
sessions from the database layer and coordinates the operations on various
repositories such as the ToDo repository.
"""

from abc import ABC, abstractmethod

from app.db.database import async_session_maker
from app.repositories.todo_repository import ToDoRepository


class IUnitOfWork(ABC):
    """Interface for Unit of Work implementations.

    This interface sets the contract for managing database transactions across
    multiple repository operations. It ensures that all changes are either
    fully committed or completely rolled back, maintaining data consistency.
    """

    todo: ToDoRepository

    @abstractmethod
    def __init__(self):
        """Initialize the Unit of Work.

        Set up any necessary pre-transaction state or configuration.
        Specific implementations should initialize data members
        required to manage the transactional context.
        """

        ...

    @abstractmethod
    async def __aenter__(self):
        """Enter the asynchronous transaction context.

        On entering, establish a new asynchronous session and prepare
        repository instances for transactional operations.
        """

        ...

    @abstractmethod
    async def __aexit__(self, *args):
        """Exit the asynchronous transaction context.

        On exit, determine if the transaction was successful or if an error
        occurred. Ensure that changes are either committed or rolled back,
        and perform any necessary cleanup.
        """

        ...

    @abstractmethod
    async def commit(self):
        """Commit the current transaction.

        Persist all pending changes to the database by committing
        the transaction.
        """

        ...

    @abstractmethod
    async def rollback(self):
        """Rollback the current transaction.

        Revert any modifications made during the transaction if an
        error occurs, ensuring that the database remains consistent.
        """

        ...


class UnitOfWork(IUnitOfWork):
    """Concrete implementation of the Unit of Work for managing transactions.

    This class manages asynchronous sessions and provides repository instances
    for performing database operations. It encapsulates the transactional
    lifecycle, ensuring proper commit and rollback behavior.
    """

    def __init__(self):
        """Initialize the UnitOfWork instance.

        This method creates a session factory using the async_session_maker
        from the database module. This factory will be used to create new
        sessions for managing transactions.
        """

        self.session_factory = async_session_maker

    async def __aenter__(self):
        """Begin a transaction context.

        Create a new asynchronous session and initialize the ToDo repository
        with it. This sets up the environment for performing transactional
        database operations.
        """

        self.session = self.session_factory()
        self.todo = ToDoRepository(self.session)

    async def __aexit__(self, *args):
        """Exit the transaction context.

        Roll back any uncommitted changes and close the session, ensuring
        no resources are left open after the transaction completes.
        """

        await self.rollback()
        await self.session.close()

    async def commit(self):
        """Commit the transaction.

        Finalize all changes made during the transaction by committing
        them to the database.
        """

        await self.session.commit()

    async def rollback(self):
        """Rollback the transaction.

        Undo any modifications made during the current transaction, reverting
        the database to its previous consistent state.
        """

        await self.session.rollback()
