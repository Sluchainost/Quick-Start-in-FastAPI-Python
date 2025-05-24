# pylint: disable=no-value-for-parameter

"""
This module provides example asynchronous selection/query methods for retrieving user data
from the database using the UserDAO class and the scientific project's session management pattern.

Each function demonstrates a different approach to querying users:
- Selecting all users.
- Selecting user IDs and usernames.
- Selecting full user info by ID.
- Selecting full user info by both ID and email.

All functions are decorated with the @connection decorator for robust session and transaction management.
"""

from typing import Sequence

from asyncio import run

from pydantic import EmailStr, create_model

from sqlalchemy import Row

from sqlalchemy.ext.asyncio import AsyncSession

from .dao.dao import UserDAO

from .dao.session_maker import connection

from .models import User

from .schemas import UserPydantic

# from schemas import UsernameIdPydantic


@connection(commit=False)
async def select_all_users(session: AsyncSession) -> Sequence[User]:
    """
    Retrieve all users from the database.

    Args:
        session (AsyncSession): The SQLAlchemy async session (injected by the decorator).

    Returns:
        list[User]: List of all User ORM instances.

    Example:
        all_users = run(select_all_users())
        for user in all_users:
            user_pydantic = UserPydantic.model_validate(user)
            print(user_pydantic.model_dump())
    """

    return await UserDAO.get_all_users(session)


# all_users = run(select_all_users())
#
# for i in all_users:
#     user_pydantic = UserPydantic.model_validate(i)
#
#     print(user_pydantic.model_dump())


@connection(commit=False)
async def select_username_id(
    session: AsyncSession,
) -> Sequence[Row[tuple[int, str]]]:
    """
    Retrieve all user IDs and usernames from the database.

    Args:
        session (AsyncSession): The SQLAlchemy async session (injected by the decorator).

    Returns:
        list[tuple[int, str]]: List of (id, username) tuples for all users.

    Example:
        rez = run(select_username_id())
        for i in rez:
            # If using UsernameIdPydantic:
            # rez_item = UsernameIdPydantic.model_validate(i)
            # print(rez_item.model_dump())
            print(i)
    """

    return await UserDAO.get_username_id(session)


# rez = run(select_username_id())
#
# for i in rez:
#
#    rez = UsernameIdPydantic.model_validate(i)
#
#    print(rez.model_dump())


@connection(commit=False)
async def select_full_user_info(session: AsyncSession, user_id: int) -> dict:
    """
    Retrieve full user information (including profile) by user ID.

    Args:
        session (AsyncSession): The SQLAlchemy async session (injected by the decorator).
        user_id (int): The ID of the user to retrieve.

    Returns:
        dict: Dictionary with user and profile data if found, or a message if not found.

    Example:
        info = run(select_full_user_info(user_id=1))
        print(info)
        # {'username': 'yakvenalex', 'email': 'example@example.com', 'profile': None}

        info = run(select_full_user_info(user_id=3))
        print(info)
        # {'message': 'User with ID {user_id} not found!'}

        info = run(select_full_user_info(user_id=20))
        print(info)
        # {'username': 'charlotte_scott', 'email': 'charlotte.scott@example.com', 'profile': None}
    """

    rez = await UserDAO.find_one_or_none_by_id(
        data_id=user_id, session=session
    )

    if rez:
        return UserPydantic.model_validate(rez).model_dump()

    return {"message": f"User with ID {user_id} not found!"}


# info = run(select_full_user_info(user_id=1))
# print(info)
#
# {'username': 'yakvenalex', 'email': 'example@example.com', 'profile': None}

# info = run(select_full_user_info(user_id=3))
# print(info)
#
# {'message': f'User with ID {user_id} not found!'}

# info = run(select_full_user_info(user_id=20))
# print(info)
#
# {'username': 'charlotte_scott', 'email': 'charlotte.scott@example.com', 'profile': None}


@connection(commit=False)
async def select_full_user_info_email(
    session: AsyncSession, user_id: int, email: str
) -> dict:
    """
    Retrieve full user information (including profile) by both user ID and email.

    Args:
        session (AsyncSession): The SQLAlchemy async session (injected by the decorator).
        user_id (int): The ID of the user to retrieve.
        email (str): The email address of the user to retrieve.

    Returns:
        dict: Dictionary with user and profile data if found, or a message if not found.

    Example:
        info = run(select_full_user_info_email(user_id=22, email='bob.smith@example.com'))
        print(info)
        # {'username': 'bob_smith', 'email': 'bob.smith@example.com',
        #  'profile': {'first_name': 'Bob', 'last_name': 'Smith',
        #              'age': 25, 'gender': 'male', 'profession': 'designer',
        #              'interests': ['gaming', 'photography', 'traveling'],
        #              'contacts': {'phone': '+987654321',
        #                           'email': 'bob.smith@example.com'}}}

        info = run(select_full_user_info_email(user_id=21, email='bob.smith@example.com'))
        print(info)
        # {'message': f'User with ID 21 not found!'}
    """

    # Dynamically create a Pydantic model for filtering by both id and email.
    FilterModel = create_model(
        "FilterModel", id=(int, ...), email=(EmailStr, ...)
    )

    user = await UserDAO.find_one_or_none(
        session=session, filters=FilterModel(id=user_id, email=email)
    )

    if user:
        return UserPydantic.model_validate(user).model_dump()

    return {"message": f"User with ID {user_id} not found!"}


# info = run(select_full_user_info_email(user_id=22, email='bob.smith@example.com'))
# print(info)
#
# {'username': 'bob_smith', 'email': 'bob.smith@example.com',
# 'profile': {'first_name': 'Bob', 'last_name': 'Smith',
#             'age': 25, 'gender': 'male', 'profession': 'designer',
#             'interests': ['gaming', 'photography', 'traveling'],
#             'contacts': {'phone': '+987654321',
#                          'email': 'bob.smith@example.com'}}}

info = run(
    select_full_user_info_email(user_id=21, email="bob.smith@example.com")
)
print(info)
#
# {'message': f'User with ID 21 not found!'}
