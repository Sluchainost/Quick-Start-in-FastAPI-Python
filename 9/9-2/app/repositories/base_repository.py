"""
This module implements the base repository pattern using SQLAlchemy's
asynchronous sessions. It provides an abstract repository with CRUD
operation signatures and a concrete repository implementation for
managing database records using a specified model.
"""

from abc import ABC, abstractmethod

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    """
    Abstract base class for repository implementations.

    This class defines the interface for repository operations such as
    adding a record and retrieving all records. Concrete repository
    classes must implement these methods.
    """

    @abstractmethod
    async def add_one(self, data: dict):
        """
        Add a single record to the repository.

        Args:
            data (dict): A dictionary containing field names and values
                         for the new record.

        Returns:
            The newly added record as returned by the
            underlying database operation.
        """

        raise NotImplementedError

    @abstractmethod
    async def find_all(self):
        """
        Retrieve all records from the repository.

        Returns:
            A list of all records available in the repository.
        """

        raise NotImplementedError


class Repository(AbstractRepository):
    """
    Concrete implementation of the abstract repository.

    This implementation provides methods to add a new record and retrieve
    all records from the database using SQLAlchemy's AsyncSession. The model
    attribute should be set to the specific database model class corresponding
    to the repository.
    """

    model = None

    def __init__(self, session: AsyncSession):
        """
        Initialize the repository with an asynchronous session.

        Args:
            session (AsyncSession): The SQLAlchemy asynchronous session used
                                    for database interactions.
        """

        self.session = session

    async def add_one(self, data: dict):
        """
        Insert a new record into the database and return the inserted record.

        This method constructs an SQL INSERT statement using the provided data,
        executes it, and returns the record that was
        inserted into the database.

        Args:
            data (dict): A dictionary containing field names and values for
                         the new record.

        Returns:
            The record that was inserted into the database.
        """

        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def find_all(self):
        """
        Retrieve all records for the current model from the database.

        This method constructs an SQL SELECT statement for the associated
        model, executes it, and returns a list of all records found.

        Returns:
            A list of all records associated with the model.
        """

        result = await self.session.execute(select(self.model))
        return result.scalars().all()
