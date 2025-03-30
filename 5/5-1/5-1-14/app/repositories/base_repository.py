"""Module for base repository classes providing a standard interface for async
   database operations.

This module defines an abstract base repository interface and its concrete
implementation using SQLAlchemy's asynchronous session. The repository
pattern is used to abstract and encapsulate all access to the data source,
ensuring that the rest of the application remains decoupled from the specifics
of the data persistence mechanism.
"""

from abc import ABC, abstractmethod

from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    """Abstract base class for repository implementations.

    This class defines the contract for basic database operations such as
    adding a record and retrieving all records. Concrete repository classes
    must implement these methods ensuring consistency across repository
    implementations.
    """

    @abstractmethod
    async def add_one(self, data: dict):
        """Add a single record to the database.

        Args:
            data (dict): A dictionary representing the fields and values for
                         the new record.

        Returns:
            The newly added record instance.

        Raises:
            NotImplementedError: If the method is not implemented by
                                 a subclass.
        """

        raise NotImplementedError

    @abstractmethod
    async def find_all(self):
        """Retrieve all records from the database for a specific model.

        Returns:
            A list of model instances representing the records retrieved
            from the database.

        Raises:
            NotImplementedError: If the method is not implemented by
                                 a subclass.
        """

        raise NotImplementedError

    @abstractmethod
    async def find_one(self, record_id: int):
        """Retrieve a single record by its ID

        Args:
            id(int): The unique identifier of the record to retrieve.

        Returns:
            The model instance if found, None otherwise.

        Raises:
            NotImplementedError: If the method is not implemented by
                                 a subclass.
        """

        raise NotImplementedError

    @abstractmethod
    async def update(self, record_id: int, data: dict):
        """Update a record by its ID.

        Args:
            id (int): The unique identifier of the record to update.
            data (dict): A dictionary of fields and values to update.

        Returns:
            The updated model instance.

        Raises:
            NotImplementedError: If the method is not implemented by
                                 a subclass.
        """

        raise NotImplementedError

    @abstractmethod
    async def delete(self, record_id: int):
        """Delete a record by its ID.

        Args:
            id (int): The unique identifier of the record to delete.

        Returns:
            True if the record was deleted, False otherwise.

        Raises:
            NotImplementedError: If the method is not implemented by
                                 a subclass.
        """

        raise NotImplementedError


class Repository(AbstractRepository):
    """Concrete repository implementation for generic database operations.

    This class provides a reusable implementation of the AbstractRepository
    for inserting and querying database records. The model attribute should
    be set to the specific SQLAlchemy model class that this repository will
    manage.
    """

    model = None

    def __init__(self, session: AsyncSession):
        """Initialize the Repository with an asynchronous database session.

        Args:
            session (AsyncSession): An instance of AsyncSession used for
                                    database interactions.
        """

        self.session = session

    async def add_one(self, data: dict):
        """Insert a new record into the table corresponding to the set model.

        Args:
            data (dict): A dictionary containing the field values for the new
                         record.

        Returns:
            The instance of the newly inserted model record, as returned by
            the database.
        """

        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)

        return res.scalar_one()

    async def find_all(self):
        """Query all records from the table corresponding to the set model.

        Returns:
            A list of model instances retrieved from the database.
        """

        result = await self.session.execute(select(self.model))

        return result.scalars().all()

    async def find_one(self, record_id: int):
        """Query a single record by its ID.

        Args:
            id (int): The unique identifier of the record to retrieve.

        Returns:
            The model instance if found, None otherwise.
        """

        result = await self.session.execute(
            select(self.model).where(self.model.id == record_id)
        )

        return result.scalar_one_or_none()

    async def update(self, record_id: int, data: dict):
        """Update a record by its ID.

        Args:
            id (int): The unique identifier of the record to update.
            data (dict): A dictionary of fields and values to update.

        Returns:
            The updated model instance.
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
        """ Delete a record by its ID.

        Args:
            id (int): The unique identifier of the record to delete.

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
