"""
Unit of Work pattern implementation using asynchronous SQLAlchemy sessions.

Defines an abstract interface `IUnitOfWork` and a concrete implementation `UnitOfWork`
that manages repositories and transaction lifecycle within async context managers.
"""

from abc import ABC, abstractmethod

from typing import Type, TypeVar, Self

from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from global_template.app.repositories.todo_repository import (
    ToDoRepository,
)
from global_template.app.repositories.user_repository import (
    UserRepository,
)
from global_template.app.repositories.userprofile_repository import (
    UserProfileRepository,
)
from global_template.app.repositories.tag_repository import (
    TagRepository,
)


T = TypeVar("T")


class IUnitOfWork(ABC):
    """
    Abstract base class for Unit of Work pattern.
    Defines the interface for managing database transactions and repositories.
    """

    @property
    @abstractmethod
    def todo(self) -> ToDoRepository:
        """
        Returns the ToDoRepository instance associated with this UnitOfWork.
        """

    @property
    @abstractmethod
    def user(self) -> UserRepository:
        """
        Returns the UserRepository instance associated with this UnitOfWork.
        """

    @property
    @abstractmethod
    def userprofile(self) -> UserProfileRepository:
        """
        Returns the UserProfileRepository instance associated with this UnitOfWork.
        """

    @property
    @abstractmethod
    def tag(self) -> TagRepository:
        """
        Returns the TagRepository instance associated with this UnitOfWork.
        """

    @abstractmethod
    def __init__(self) -> None:
        """
        Initializes the UnitOfWork instance.
        """

    @abstractmethod
    async def __aenter__(self) -> Self:
        """
        Enter the asynchronous context manager.
        Should initialize the session and repositories.
        """

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        Exit the asynchronous context manager.
        Commits the transaction if no exception occurred, otherwise rollbacks.
        Closes the session and cleans up resources.
        """

    @abstractmethod
    async def commit(self) -> None:
        """
        Commits the current transaction.
        """

    @abstractmethod
    async def rollback(self) -> None:
        """
        Rolls back the current transaction.
        """


class UnitOfWork(IUnitOfWork):
    """
    Concrete implementation of the UnitOfWork interface using SQLAlchemy AsyncSession.
    Manages repositories and database transactions within an async context.
    """

    def __init__(
        self, session_factory: async_sessionmaker[AsyncSession]
    ) -> None:
        """
        Initializes the UnitOfWork with a session factory.

        Args:
            session_factory: An async sessionmaker instance to create AsyncSession objects.
        """

        self._session_factory = session_factory
        self._session: AsyncSession | None = None

        self._todo: ToDoRepository | None = None
        self._user: UserRepository | None = None
        self._userprofile: UserProfileRepository | None = None
        self._tag: TagRepository | None = None

    def _get_repo(self, repo: T | None, name: str) -> T:
        """
        Helper method to safely retrieve a repository instance.

        Args:
            repo: The repository instance or None if not initialized.
            name: The name of the repository (for error messages).

        Returns:
            The repository instance if initialized.

        Raises:
            RuntimeError: If the repository is accessed before initialization.
        """

        if repo is None:
            raise RuntimeError(
                f"UnitOfWork is not initialized. Use 'async with' context. Repo: {name}"
            )
        return repo

    def _clear_repos(self) -> None:
        """
        Clears all repository references to release resources.
        """

        self._todo = None
        self._user = None
        self._userprofile = None
        self._tag = None

    @property
    def todo(self) -> ToDoRepository:
        """
        Returns the ToDoRepository instance.

        Raises:
            RuntimeError: If accessed outside of an active UnitOfWork context.
        """

        return self._get_repo(self._todo, "todo")

    @property
    def user(self) -> UserRepository:
        """
        Returns the UserRepository instance.

        Raises:
            RuntimeError: If accessed outside of an active UnitOfWork context.
        """

        return self._get_repo(self._user, "user")

    @property
    def userprofile(self) -> UserProfileRepository:
        """
        Returns the UserProfileRepository instance.

        Raises:
            RuntimeError: If accessed outside of an active UnitOfWork context.
        """

        return self._get_repo(self._userprofile, "userprofile")

    @property
    def tag(self) -> TagRepository:
        """
        Returns the TagRepository instance.

        Raises:
            RuntimeError: If accessed outside of an active UnitOfWork context.
        """

        return self._get_repo(self._tag, "tag")

    async def __aenter__(self) -> Self:
        """
        Asynchronous context manager entry.
        Creates a new session and initializes repositories.

        Returns:
            The UnitOfWork instance.
        """

        self._session = self._session_factory()

        # Initialize repositories with the session
        self._todo = ToDoRepository(self._session)
        self._user = UserRepository(self._session)
        self._userprofile = UserProfileRepository(self._session)
        self._tag = TagRepository(self._session)

        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        Asynchronous context manager exit.
        Commits the session if no exception occurred, otherwise rollbacks.
        Closes the session and clears repositories.

        Args:
            exc_type: Exception type if raised, else None.
            exc_val: Exception instance if raised, else None.
            exc_tb: Traceback if exception raised, else None.
        """

        if self._session is None:
            return

        try:
            if exc_type:
                await self._session.rollback()
            else:
                await self._session.commit()
        finally:
            await self._session.close()
            self._session = None
            self._clear_repos()

    async def commit(self) -> None:
        """
        Commits the current transaction.

        Raises:
            RuntimeError: If the session is not initialized.
        """

        if self._session is None:
            raise RuntimeError("Session is not initialized.")

        await self._session.commit()

    async def rollback(self) -> None:
        """
        Rolls back the current transaction.

        Raises:
            RuntimeError: If the session is not initialized.
        """

        if self._session is None:
            raise RuntimeError("Session is not initialized.")

        await self._session.rollback()
