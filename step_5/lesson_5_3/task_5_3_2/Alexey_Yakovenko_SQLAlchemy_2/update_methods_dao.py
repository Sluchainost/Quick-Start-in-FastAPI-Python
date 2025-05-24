# pylint: disable=no-value-for-parameter

"""
This module provides example asynchronous update methods for modifying user and profile data
in the database using both direct SQLAlchemy statements and DAO-based patterns.

Each function demonstrates a different approach to updating records:
- Updating a user's username by ID.
- Updating a user's username and email by ID.
- Mass-updating the age field for all profiles with a given last name (direct SQL).
- Mass-updating the age field for all profiles with a given last name (DAO pattern).

All functions are decorated with the @connection decorator for robust session and transaction management.
"""

import asyncio

from pydantic import create_model, EmailStr

from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Profile

from .dao.dao import ProfileDAO, UserDAO
from .dao.session_maker import connection


@connection(commit=True)
async def update_username(
    session: AsyncSession, user_id: int, new_username: str
) -> None:
    """
    Update the username of a user by their ID using the UserDAO.

    Args:
        session (AsyncSession): The SQLAlchemy async session (injected by the decorator).
        user_id (int): The ID of the user to update.
        new_username (str): The new username to set.

    Returns:
        None

    Example:
        asyncio.run(update_username(user_id=1, new_username='yakvenalexx'))
    """

    # Dynamically create a Pydantic model for the updated value.
    ValueModel = create_model("ValueModel", username=(str, ...))

    # Use the DAO's update_one_by_id method for the update.
    await UserDAO.update_one_by_id(
        session=session,
        data_id=user_id,
        values=ValueModel(username=new_username),
    )


# asyncio.run(update_username(user_id=1, new_username='yakvenalexx'))


@connection(commit=True)
async def update_user(
    session: AsyncSession, user_id: int, new_username: str, email: int
) -> None:
    """
    Update both the username and email of a user by their ID using the UserDAO.

    Args:
        session (AsyncSession): The SQLAlchemy async session (injected by the decorator).
        user_id (int): The ID of the user to update.
        new_username (str): The new username to set.
        email (str): The new email address to set.

    Returns:
        None

    Example:
        asyncio.run(update_user(user_id=1, email='mail@mail.ru', new_username='admin'))
    """

    # Dynamically create a Pydantic model for the updated values.
    ValueModel = create_model(
        "ValueModel", username=(str, ...), email=(EmailStr, ...)
    )

    # Use the DAO's update_one_by_id method for the update.
    await UserDAO.update_one_by_id(
        session=session,
        data_id=user_id,
        values=ValueModel(username=new_username, email=email),
    )


# asyncio.run(update_user(user_id=1, email='mail@mail.ru', new_username='admin'))


@connection(commit=True)
async def update_age_mass(
    session: AsyncSession, new_age: int, last_name: str
) -> int:
    """
    Mass-update the age field for all profiles with a given last name using a direct SQLAlchemy statement.

    Args:
        session (AsyncSession): The SQLAlchemy async session (injected by the decorator).
        new_age (int): The new age value to set.
        last_name (str): The last name to filter profiles by.

    Returns:
        int: The number of records updated.

    Example:
        asyncio.run(update_age_mass(new_age=22, last_name='Smith'))
    """

    try:
        # Construct an UPDATE statement for the Profile table.
        stmt = (
            update(Profile).filter_by(last_name=last_name).values(age=new_age)
        )

        # Execute the update and get the number of affected rows.
        result = await session.execute(stmt)
        updated_count = result.rowcount

        print(f"Updated {updated_count} records")

        return updated_count
    except SQLAlchemyError as e:
        print(f"Error updating profiles: {e}")
        raise e


# asyncio.run(update_age_mass(new_age=22, last_name='Smith'))


@connection(commit=True)
async def update_age_mass_dao(
    session: AsyncSession, new_age: int, last_name: str
) -> None:
    """
    Mass-update the age field for all profiles with a given last name using the ProfileDAO.

    This approach uses dynamic Pydantic models for both the filter criteria and the updated values,
    demonstrating the DAO's generic update_many method.

    Args:
        session (AsyncSession): The SQLAlchemy async session (injected by the decorator).
        new_age (int): The new age value to set.
        last_name (str): The last name to filter profiles by.

    Returns:
        None

    Example:
        asyncio.run(update_age_mass_dao(new_age=33, last_name='Smith'))
    """

    # Dynamically create Pydantic models for filter criteria and update values.
    filter_criteria = create_model("FilterModel", last_name=(str, ...))
    values = create_model("ValuesModel", age=(int, ...))

    # Use the DAO's update_many method for the update.
    await ProfileDAO.update_many(
        session=session,
        filter_criteria=filter_criteria(last_name=last_name),
        values=values(age=new_age),
    )


asyncio.run(update_age_mass_dao(new_age=33, last_name="Smith"))
