# pylint: disable=no-value-for-parameter

"""
This module provides example asynchronous methods for adding users to the database
using the UserDAO class and the scientific project's session management pattern.

Each function demonstrates a different approach to user creation:
- Adding a single user with minimal fields.
- Adding multiple users in a batch.
- Adding a user with a complete profile in a single transaction.

All functions are decorated with the @connection decorator for robust session and transaction management.
"""

from typing import List, cast

from asyncio import run

from pydantic import BaseModel

from sqlalchemy.ext.asyncio import AsyncSession

from .dao.dao import UserDAO

from .dao.session_maker import connection

from .sql_enums import GenderEnum, ProfessionEnum


@connection(commit=False)
async def add_one(user_data: dict, session: AsyncSession) -> int:
    """
    Add a single user to the database using the UserDAO.

    Args:
        user_data (dict): Dictionary containing user fields (e.g., 'username', 'email', 'password').
        session (AsyncSession): The SQLAlchemy async session (injected by the decorator).

    Returns:
        int: The ID of the newly created user.

    Example:
        one_user = {
            "username": "oliver_jackson",
            "email": "oliver.jackson@example.com",
            "password": "jackson123"
        }
        run(add_one(user_data=one_user))
    """

    # Use the generic DAO add method to create a new user.
    new_user = await UserDAO.add(session=session, **user_data)

    print(f"Added new user with ID: {new_user.id}")

    return cast(int, new_user.id)


# one_user: dict[str, str] = {"username": "oliver_jackson",
#                            "email": "oliver.jackson@example.com",
#                            "password": "jackson123"}

# run(add_one(user_data=one_user)) # type: ignore


@connection(commit=False)
async def add_many_users(
    users_data: List[BaseModel], session: AsyncSession
) -> List[int]:
    """
    Add multiple users to the database in a single batch operation.

    Args:
        users_data (List[dict]): List of dictionaries, each containing user fields.
        session (AsyncSession): The SQLAlchemy async session (injected by the decorator).

    Returns:
        List[int]: List of IDs for the newly created users.

    Example:
        users = [
            {"username": "amelia_davis", "email": "amelia.davis@example.com", "password": "davispassword"},
            {"username": "lucas_white", "email": "lucas.white@example.com", "password": "whiteSecure"},
            ...
        ]
        run(add_many_users(users_data=users))
    """

    # Use the generic DAO add_many method to create multiple users at once.
    new_users = await UserDAO.add_many(session=session, instances=users_data)

    user_ilds_list = [user.id for user in new_users]

    print(f"Added new users with ID: {user_ilds_list}")

    return user_ilds_list


# users = [
#    {"username": "amelia_davis", "email": "amelia.davis@example.com",
#     "password": "davispassword"},
#    {"username": "lucas_white", "email": "lucas.white@example.com",
#     "password": "whiteSecure"},
#    {"username": "mia_moore", "email": "mia.moore@example.com",
#     "password": "moorepass098"},
#    {"username": "benjamin_hall", "email": "benjamin.hall@example.com",
#     "password": "hallben123"},
#    {"username": "sophia_hill", "email": "sophia.hill@example.com",
#     "password": "hillSophia999"},
#    {"username": "liam_green", "email": "liam.green@example.com",
#     "password": "greenSecure789"},
#    {"username": "isabella_clark", "email": "isabella.clark@example.com",
#     "password": "clarkIsabella001"},
#    {"username": "ethan_baker", "email": "ethan.baker@example.com",
#     "password": "bakerEthan555"},
#    {"username": "charlotte_scott", "email": "charlotte.scott@example.com",
#     "password": "scottcharl333"},
#    {"username": "logan_young", "email": "logan.young@example.com",
#     "password": "younglogan876"}
# ]

# run(add_many_users(users_data=users)) # type: ignore


@connection(commit=False)
async def add_full_user(user_data: dict, session: AsyncSession) -> int:
    """
    Add a user with a complete profile in a single transaction.

    This function uses the UserDAO's add_user_with_profile method to create both
    the User and their associated Profile atomically.

    Args:
        user_data (dict): Dictionary containing all required and optional fields for both User and Profile.
            Required keys: username, email, password, first_name, gender.
            Optional keys: last_name, age, profession, interests, contacts.
        session (AsyncSession): The SQLAlchemy async session (injected by the decorator).

    Returns:
        int: The ID of the newly created user.

    Example:
        user_data_bob = {
            "username": "bob_smith",
            "email": "bob.smith@example.com",
            "password": "bobsecure456",
            "first_name": "Bob",
            "last_name": "Smith",
            "age": 25,
            "gender": GenderEnum.MALE,
            "profession": ProfessionEnum.DESIGNER,
            "interests": ["gaming", "photography", "traveling"],
            "contacts": {"phone": "+987654321", "email": "bob.smith@example.com"}
        }
        run(add_full_user(user_data=user_data_bob))
    """

    # Use the DAO's custom method to create both user and profile in one transaction.
    new_user = await UserDAO.add_user_with_profile(
        session=session, user_data=user_data
    )

    print(f"Added new user with ID: {new_user.id}")

    return new_user.id


user_data_bob = {
    "username": "bob_smith",
    "email": "bob.smith@example.com",
    "password": "bobsecure456",
    "first_name": "Bob",
    "last_name": "Smith",
    "age": 25,
    "gender": GenderEnum.MALE,
    "profession": ProfessionEnum.DESIGNER,
    "interests": ["gaming", "photography", "traveling"],
    "contacts": {"phone": "+987654321", "email": "bob.smith@example.com"},
}

run(add_full_user(user_data=user_data_bob))  # type: ignore
