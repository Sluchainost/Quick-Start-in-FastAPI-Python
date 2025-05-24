"""Unit of Work pattern for managing database transactions."""

from abc import ABC, abstractmethod

from app.db.database import async_session_maker
from app.repositories.todo_repository import ToDoRepository


class IUnitOfWork(ABC):
    """
    Interface for Unit of Work pattern.

    Manages repositories and database transactions.
    """

    todo: ToDoRepository

    @abstractmethod
    def __init__(self):
        """
        Initialize the Unit of Work.
        """

    @abstractmethod
    async def __aenter__(self):
        """
        Enter the runtime context and clean up resources.
        """

    @abstractmethod
    async def __aexit__(self, *args):
        """
        Exit the runtime context and clean up resources.
        """

    @abstractmethod
    async def commit(self):
        """
        Commit the current transaction.
        """

    @abstractmethod
    async def rollback(self):
        """
        Roll back the current transaction.
        """


class UnitOfWork(IUnitOfWork):
    """
    Implementation of the Unit of Work pattern.

    Handles session lifecycle and provides access to repositories.
    """

    def __init__(self):
        """
        Initialize the UnitOfWork with a new session.
        """

        self.session_factory = async_session_maker
        self.session = self.session_factory()

    async def __aenter__(self):
        """
        Enter the runtime context and initialize repositories.
        """

        self.todo = ToDoRepository(self.session)

    async def __aexit__(self, *args):
        """
        Roll back any uncommitted changes and close the session.
        """

        await self.rollback()
        await self.session.close()

    async def commit(self):
        """
        Commit the current transaction.
        """

        await self.session.commit()

    async def rollback(self):
        """
        Roll back the current transaction.
        """

        await self.session.rollback()
