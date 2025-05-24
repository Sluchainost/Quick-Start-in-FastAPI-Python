"""Base repository classes for CRUD operations using SQLAlchemy."""

from abc import ABC, abstractmethod

from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    """
    Abstract base class for repository pattern.

    Defines the interface for CRUD operations that all repositories
    must implement.
    """

    @abstractmethod
    async def add_one(self, data: dict):
        """
        Add a new record to the database.

        Args:
            data (dict): Data for the new record.

        Returns:
            The created record instance.
        """

        raise NotImplementedError

    @abstractmethod
    async def find_one(self, record_id: int):
        """
        Retrieve a single record by its ID.

        Args:
            record_id (int): The ID of the record to retrieve.

        Returns:
            The record instance if found, else None.
        """

        raise NotImplementedError

    @abstractmethod
    async def update(self, record_id: int, data: dict):
        """
        Update an existing record by its ID.

        Args:
            record_id (int): The ID of the record to update.
            data (dict): Fields to update.

        Returns:
            The updated record instance if found, else None.
        """

        raise NotImplementedError

    @abstractmethod
    async def delete(self, record_id: int):
        """
        Delete a record by its ID.

        Args:
            record_id (int): The ID of the record to delete.

        Returns:
            True if the record was deleted, False otherwise.
        """

        raise NotImplementedError


class Repository(AbstractRepository):
    """
    Generic repository implementation for SQLAlchemy models.

    Provides async CRUD operations for a given SQLAlchemy model.
    """

    model = None

    def __init__(self, session: AsyncSession):
        """
        Initialize the repository with a database session.

        Args:
            session (AsyncSession): SQLAlchemy async session.
        """

        self.session = session

    async def add_one(self, data: dict):
        """
        Add a new record to the database.

        Args:
            data (dict): Data for the new record.

        Returns:
            The created record instance.
        """

        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)

        return res.scalar_one()

    async def find_one(self, record_id: int):
        """
        Retrieve a single record by its ID.

        Args:
            record_id (int): The ID of the record to retrieve.

        Returns:
            The record instance if found, else None.
        """

        result = await self.session.execute(
            select(self.model).where(self.model.id == record_id)
        )

        return result.scalar_one_or_none()

    async def update(self, record_id: int, data: dict):
        """
        Update an existing record by its ID.

        Args:
            record_id (int): The ID of the record to update.
            data (dict): Fields to update.

        Returns:
            The updated record instance if found, else None.
        """

        stmt = (
            update(self.model)
            .where(self.model.id == record_id)
            .values(**data)
            .returning(self.model)
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def delete(self, record_id: int):
        """
        Delete a record by its ID.

        Args:
            record_id (int): The ID of the record to delete.

        Returns:
            True if the record was deleted, False otherwise.
        """

        stmt = (
            delete(self.model)
            .where(self.model.id == record_id)
            .returning(self.model.id)
        )

        result = await self.session.execute(stmt)

        deleted_id = result.scalar_one_or_none()

        return deleted_id is not None
