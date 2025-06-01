# pylint: disable=no-value-for-parameter

"""
This module provides example asynchronous delete methods for removing user records
from the database using both direct SQLAlchemy statements and DAO-based patterns.

Each function demonstrates a different approach to deleting records:
- Deleting a user by ID (direct SQLAlchemy).
- Deleting a user by ID using the DAO.
- Deleting users whose usernames start with a specific prefix.
- Deleting users by password using the DAO and dynamic Pydantic filters.

All functions are decorated with the @connection decorator for robust session and transaction management.
"""

import asyncio

from pydantic import create_model

from sqlalchemy import delete

from sqlalchemy.ext.asyncio import AsyncSession

from step_5.lesson_5_3.task_5_3_2.Alexey_Yakovenko_SQLAlchemy_2.dao.dao import (
    UserDAO,
)
from step_5.lesson_5_3.task_5_3_2.Alexey_Yakovenko_SQLAlchemy_2.dao.session_maker import (
    connection,
)

from step_5.lesson_5_3.task_5_3_2.Alexey_Yakovenko_SQLAlchemy_2.models import (
    User,
)


@connection(commit=True)
async def delete_user_by_id(session: AsyncSession, user_id: int) -> None:
    """
    Delete a user from the database by their unique ID using direct SQLAlchemy ORM.

    Args:
        session (AsyncSession): The SQLAlchemy async session (injected by the decorator).
        user_id (int): The ID of the user to delete.

    Returns:
        None

    Example:
        asyncio.run(delete_user_by_id(user_id=6))
    """

    user = await session.get(User, user_id)

    if user:
        await session.delete(user)
        # The session will be committed by the decorator.


# asyncio.run(delete_user_by_id(user_id=6))


@connection(commit=True)
async def delete_user_by_id_dao(session: AsyncSession, user_id: int) -> None:
    """
    Delete a user from the database by their unique ID using the UserDAO.

    Args:
        session (AsyncSession): The SQLAlchemy async session (injected by the decorator).
        user_id (int): The ID of the user to delete.

    Returns:
        None

    Example:
        asyncio.run(delete_user_by_id_dao(user_id=10))
    """

    await UserDAO.delete_one_by_id(session=session, data_id=user_id)
    # The session will be committed by the decorator.


# asyncio.run(delete_user_by_id_dao(user_id=10))


@connection(commit=True)
async def delete_user_username_ja(
    session: AsyncSession, start_letter: str = "ja"
):
    """
    Delete all users whose usernames start with a given prefix using a direct SQLAlchemy DELETE statement.

    Args:
        session (AsyncSession): The SQLAlchemy async session (injected by the decorator).
        start_letter (str): The prefix to match usernames (default: 'ja').

    Returns:
        None

    Example:
        asyncio.run(delete_user_username_ja())
        # Deletes all users whose usernames start with 'ja'
    """

    stmt = delete(User).where(User.username.like(f"{start_letter}%"))

    await session.execute(stmt)
    # The session will be committed by the decorator.


# asyncio.run(delete_user_username_ja())


@connection(commit=True)
async def delete_user_by_password(
    session: AsyncSession, password: str
) -> None:
    """
    Delete all users with a specific password using the UserDAO and a dynamic Pydantic filter.

    Args:
        session (AsyncSession): The SQLAlchemy async session (injected by the decorator).
        password (str): The password to match for deletion.

    Returns:
        None

    Example:
        asyncio.run(delete_user_by_password(password='asdasd'))
    """

    # Dynamically create a Pydantic model for filtering by password.
    filter_criteria = create_model("FilterModel", password=(str, ...))

    await UserDAO.delete_many(
        session=session, filters=filter_criteria(password=password)
    )
    # The session will be committed by the decorator.


asyncio.run(delete_user_by_password(password="asdasd"))
