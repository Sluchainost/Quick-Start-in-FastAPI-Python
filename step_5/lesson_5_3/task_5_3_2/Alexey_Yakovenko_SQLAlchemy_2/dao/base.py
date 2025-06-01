"""
This module defines a generic, asynchronous Data Access Object (DAO) base class for SQLAlchemy models.
It provides reusable CRUD operations for any model that inherits from the project's declarative Base.
Pydantic models are used for input validation and serialization.

Features:
- Generic typing for type safety and reusability.
- Asynchronous methods for efficient database interaction.
- Comprehensive error handling for robust scientific workflows.
"""

from typing import List, TypeVar, Generic, cast

from pydantic import BaseModel

from sqlalchemy import select, update, delete

from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy.ext.asyncio import AsyncSession

from step_5.lesson_5_3.task_5_3_2.Alexey_Yakovenko_SQLAlchemy_2.dao.database import (
    Base,
)


# Type variable for generic DAO, bound to SQLAlchemy Base.
T = TypeVar("T", bound=Base)


class BaseDAO(Generic[T]):
    """
    Generic asynchronous DAO base class for SQLAlchemy models.

    This class provides standard CRUD operations (Create, Read, Update, Delete)
    for any SQLAlchemy model. All methods are asynchronous and expect an
    AsyncSession for database interaction.

    Attributes:
        model (type[T]): The SQLAlchemy model class associated with this DAO.
    """

    model: type[T]

    @classmethod
    async def add(cls, session: AsyncSession, values: BaseModel) -> T:
        """
        Add a single new record to the database.

        Args:
            session (AsyncSession): The active SQLAlchemy async session.
            values (BaseModel): Pydantic model containing validated data for the new record.

        Returns:
            T: The newly created SQLAlchemy model instance.

        Raises:
            SQLAlchemyError: If the operation fails.
        """

        # Convert Pydantic model to dictionary, excluding unset fields.
        values_dict = values.model_dump(exclude_unset=True)

        new_instance = cls.model(**values_dict)

        session.add(new_instance)

        try:
            await session.flush()  # Flush to assign PK and catch DB errors early.
        except SQLAlchemyError as e:
            await session.rollback()
            raise e

        return cast(T, new_instance)

    @classmethod
    async def add_many(
        cls, session: AsyncSession, instances: List[BaseModel]
    ) -> List[T]:
        """
        Add multiple new records to the database in a single batch.

        Args:
            session (AsyncSession): The active SQLAlchemy async session.
            instances (List[BaseModel]): List of Pydantic models with validated data.

        Returns:
            List[T]: List of newly created SQLAlchemy model instances.

        Raises:
            SQLAlchemyError: If the operation fails.
        """

        values_list = [
            item.model_dump(exclude_unset=True) for item in instances
        ]

        new_instances = [cls.model(**values) for values in values_list]

        session.add_all(new_instances)

        try:
            await session.flush()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e

        return new_instances

    @classmethod
    async def find_one_or_none_by_id(
        cls, data_id: int, session: AsyncSession
    ) -> T | None:
        """
        Retrieve a single record by its primary key.

        Args:
            data_id (int): The primary key of the record.
            session (AsyncSession): The active SQLAlchemy async session.

        Returns:
            T | None: The found model instance, or None if not found.

        Raises:
            SQLAlchemyError: If the operation fails.
        """

        try:
            return cast(T | None, await session.get(cls.model, data_id))
        except SQLAlchemyError as e:
            print(f"Error occurred: {e}")
            raise e

    @classmethod
    async def find_one_or_none(
        cls, session: AsyncSession, filters: BaseModel
    ) -> T | None:
        """
        Retrieve a single record matching the provided filters.

        Args:
            session (AsyncSession): The active SQLAlchemy async session.
            filters (BaseModel): Pydantic model with filter criteria.

        Returns:
            T | None: The found model instance, or None if not found.

        Raises:
            SQLAlchemyError: If the operation fails.
        """

        filter_dict = filters.model_dump(exclude_unset=True)

        try:
            query = select(cls.model).filter_by(**filter_dict)

            result = await session.execute(query)

            record = result.scalar_one_or_none()

            return cast(T | None, record)
        except SQLAlchemyError as e:
            raise e

    @classmethod
    async def find_all(
        cls, session: AsyncSession, filters: BaseModel | None
    ) -> List[T]:
        """
        Retrieve all records matching the provided filters.

        Args:
            session (AsyncSession): The active SQLAlchemy async session.
            filters (BaseModel | None): Pydantic model with filter criteria, or None for all records.

        Returns:
            List[T]: List of found model instances.

        Raises:
            SQLAlchemyError: If the operation fails.
        """

        if filters:
            filter_dict = filters.model_dump(exclude_unset=True)
        else:
            filter_dict = {}

        try:
            query = select(cls.model).filter_by(**filter_dict)

            result = await session.execute(query)

            records = result.scalars().all()

            return cast(List[T], records)
        except SQLAlchemyError as e:
            raise e

    @classmethod
    async def update_one_by_id(
        cls, session: AsyncSession, data_id: int, values: BaseModel
    ) -> None:
        """
        Update a single record by its primary key.

        Args:
            session (AsyncSession): The active SQLAlchemy async session.
            data_id (int): The primary key of the record to update.
            values (BaseModel): Pydantic model with updated values.

        Raises:
            SQLAlchemyError: If the operation fails.
        """

        values_dict = values.model_dump(exclude_unset=True)

        try:
            record = await session.get(cls.model, data_id)

            # Update only the provided fields.
            for key, value in values_dict.items():
                setattr(record, key, value)

            await session.flush()
        except SQLAlchemyError as e:
            print(e)
            raise e

    @classmethod
    async def update_many(
        cls,
        session: AsyncSession,
        filter_criteria: BaseModel,
        values: BaseModel,
    ) -> int:
        """
        Update multiple records matching the filter criteria.

        Args:
            session (AsyncSession): The active SQLAlchemy async session.
            filter_criteria (BaseModel): Pydantic model with filter criteria.
            values (BaseModel): Pydantic model with updated values.

        Returns:
            int: Number of rows updated.

        Raises:
            SQLAlchemyError: If the operation fails.
        """

        filter_dict = filter_criteria.model_dump(exclude_unset=True)
        values_dict = values.model_dump(exclude_unset=True)

        try:
            stmt = (
                update(cls.model)
                .filter_by(**filter_dict)
                .values(**values_dict)
            )

            result = await session.execute(stmt)

            await session.flush()

            return result.rowcount
        except SQLAlchemyError as e:
            print(f"Error in mass update: {e}")
            raise e

    @classmethod
    async def delete_one_by_id(
        cls, data_id: int, session: AsyncSession
    ) -> None:
        """
        Delete a single record by its primary key.

        Args:
            data_id (int): The primary key of the record to delete.
            session (AsyncSession): The active SQLAlchemy async session.

        Raises:
            SQLAlchemyError: If the operation fails.
        """

        try:
            data = await session.get(cls.model, data_id)

            if data:
                await session.delete(data)
                await session.flush()
        except SQLAlchemyError as e:
            print(f"Error occurred: {e}")
            raise e

    @classmethod
    async def delete_many(
        cls, session: AsyncSession, filters: BaseModel | None
    ) -> int:
        """
        Delete multiple records matching the provided filters.

        Args:
            session (AsyncSession): The active SQLAlchemy async session.
            filters (BaseModel | None): Pydantic model with filter criteria, or None to delete all records.

        Returns:
            int: Number of rows deleted.

        Raises:
            SQLAlchemyError: If the operation fails.
        """

        if filters:
            filter_dict = filters.model_dump(exclude_unset=True)

            stmt = delete(cls.model).filter_by(**filter_dict)
        else:
            stmt = delete(cls.model)

        try:
            result = await session.execute(stmt)

            await session.flush()

            return result.rowcount
        except SQLAlchemyError as e:
            print(f"Error occurred: {e}")
            raise e
