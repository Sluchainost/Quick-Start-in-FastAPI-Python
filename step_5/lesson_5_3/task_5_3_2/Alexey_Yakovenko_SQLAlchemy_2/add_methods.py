# pylint: disable=no-value-for-parameter, too-many-positional-arguments

"""
This module provides example asynchronous methods for creating users and profiles
using SQLAlchemy ORM in a scientific project context.

Each function demonstrates a different pattern for transaction management,
error handling, and relationship creation, with detailed documentation and
comments for reproducibility and future reference.
"""

from asyncio import run

from sqlalchemy.ext.asyncio import AsyncSession

from step_5.lesson_5_3.task_5_3_2.Alexey_Yakovenko_SQLAlchemy_2.dao.session_maker import (
    connection,
)

from step_5.lesson_5_3.task_5_3_2.Alexey_Yakovenko_SQLAlchemy_2.models import (
    Profile,
    User,
    GenderEnum,
    ProfessionEnum,
)


@connection(commit=False)
async def create_user_example_1(
    username: str, email: str, password: str, session: AsyncSession
) -> int:
    """
    Create a new user and persist it to the database.

    This example demonstrates the simplest case: creating a User instance,
    adding it to the session, and committing the transaction.

    Args:
        username (str): The user's unique username.
        email (str): The user's unique email address.
        password (str): The user's password (should be hashed in production).
        session (AsyncSession): The SQLAlchemy async session (injected by the decorator).

    Returns:
        int: The ID of the newly created user.

    Example:
        new_user_id = run(create_user_example_1(
            username="yakvenalex",
            email="example@example.com",
            password="asdasd"
        ))
        print(f"New user created with ID {new_user_id}")
    """

    user = User(username=username, email=email, password=password)
    session.add(user)
    await session.commit()  # Commit to persist the user and assign an ID.
    return user.id


# new_user_id = run(create_user_example_1(username="yakvenalex",
#                                        email="example@example.com",
#                                        password="asdasd"))
# print(f"New user created with ID {new_user_id}")


@connection(commit=False)
async def get_user_by_id_example_2(
    username: str,
    email: str,
    password: str,
    first_name: str,
    last_name: str | None,
    age: str | None,
    gender: GenderEnum,
    profession: ProfessionEnum | None,
    interests: list | None,
    contacts: dict | None,
    session: AsyncSession,
) -> dict[str, int]:
    """
    Create a new user and immediately create an associated profile.

    This example demonstrates sequential creation of a User and a Profile,
    with two separate commits. The Profile references the User's ID.

    Args:
        username (str): The user's unique username.
        email (str): The user's unique email address.
        password (str): The user's password.
        first_name (str): The user's first name.
        last_name (str | None): The user's last name (optional).
        age (str | None): The user's age (optional).
        gender (GenderEnum): The user's gender.
        profession (ProfessionEnum | None): The user's profession (optional).
        interests (list | None): List of user's interests (optional).
        contacts (dict | None): Arbitrary contact information (optional).
        session (AsyncSession): The SQLAlchemy async session.

    Returns:
        dict[str, int]: Dictionary with 'user_id' and 'profile_id'.

    Example:
        user_profile = run(get_user_by_id_example_2(
            username="john_doe",
            email="john.doe@example.com",
            password="password123",
            first_name="John",
            last_name="Doe",
            age=28,
            gender=GenderEnum.MALE,
            profession=ProfessionEnum.ENGINEER,
            interests=["hiking", "photography", "coding"],
            contacts={"phone": "+123456789", "email": "john.doe@example.com"},
        ))
    """

    user = User(username=username, email=email, password=password)

    session.add(user)

    await session.commit()  # Commit to assign user.id

    profile = Profile(
        user_id=user.id,
        first_name=first_name,
        last_name=last_name,
        age=age,
        gender=gender,
        profession=profession,
        interests=interests,
        contacts=contacts,
    )

    session.add(profile)

    await session.commit()  # Commit to persist the profile

    print(
        f"Created user with ID {user.id} and assigned profile with ID {profile.id}"
    )

    return {"user_id": user.id, "profile_id": profile.id}


# user_profile = run(get_user_by_id_example_2(
#    username="john_doe",
#    email="john.doe@example.com",
#    password="password123",
#    first_name="John",
#    last_name="Doe",
#    age=28,
#    gender=GenderEnum.MALE,
#    profession=ProfessionEnum.ENGINEER,
#    interests=["hiking", "photography", "coding"],
#    contacts={"phone": "+123456789", "email": "john.doe@example.com"},
# ))


@connection(commit=False)
async def get_user_by_id_example_3(
    username: str,
    email: str,
    password: str,
    first_name: str,
    last_name: str,
    age: str | None,
    gender: GenderEnum,
    profession: ProfessionEnum | None,
    interests: list | None,
    contacts: dict | None,
    session: AsyncSession,
) -> dict[str, int]:
    """
    Create a new user and associated profile in a single transaction with error handling.

    This example demonstrates the use of session.flush() to assign the User's ID
    before creating the Profile, and wraps the operation in a try/except block
    for robust error handling and rollback.

    Args:
        username (str): The user's unique username.
        email (str): The user's unique email address.
        password (str): The user's password.
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        age (str | None): The user's age (optional).
        gender (GenderEnum): The user's gender.
        profession (ProfessionEnum | None): The user's profession (optional).
        interests (list | None): List of user's interests (optional).
        contacts (dict | None): Arbitrary contact information (optional).
        session (AsyncSession): The SQLAlchemy async session.

    Returns:
        dict[str, int]: Dictionary with 'user_id' and 'profile_id'.

    Raises:
        Exception: Any exception during the transaction will trigger a rollback.

    Example:
        user_profile = run(get_user_by_id_example_3(
            username="john_doe_3",
            email="john.doe@example.com_3",
            password="password123_3",
            first_name="John_3",
            last_name="Doe_3",
            age=29,
            gender=GenderEnum.MALE,
            profession=ProfessionEnum.ENGINEER,
            interests=["hiking_3", "photography_3", "coding_3"],
            contacts={"phone_3": "+123456789_3", "email_3": "john.doe@example.com_3"},
        ))
    """

    try:
        user = User(username=username, email=email, password=password)

        session.add(user)

        await session.flush()  # Flush to assign user.id without committing

        profile = Profile(
            user_id=user.id,
            first_name=first_name,
            last_name=last_name,
            age=age,
            gender=gender,
            profession=profession,
            interests=interests,
            contacts=contacts,
        )

        session.add(profile)

        await session.commit()  # Commit both user and profile atomically

        print(
            f"Created user with ID {user.id} and assigned profile with ID {profile.id}"
        )

        return {"user_id": user.id, "profile_id": profile.id}

    except Exception as e:
        await session.rollback()
        raise e  # Propagate the exception for upstream handling


# user_profile = run(get_user_by_id_example_3(
#    username="john_doe_3",
#    email="john.doe@example.com_3",
#    password="password123_3",
#    first_name="John_3",
#    last_name="Doe_3",
#    age=29,
#    gender=GenderEnum.MALE,
#    profession=ProfessionEnum.ENGINEER,
#    interests=["hiking_3", "photography_3", "coding_3"],
#    contacts={"phone_3": "+123456789_3", "email_3": "john.doe@example.com_3"},
# )) # type: ignore


@connection(commit=False)
async def create_user_example_4(
    users_data: list[dict], session: AsyncSession
) -> list[int]:
    """
    Batch-create multiple users in a single transaction.

    This example demonstrates how to efficiently create several User instances
    at once using session.add_all(), and commit the transaction to persist all users.

    Args:
        users_data (list[dict]): List of dictionaries, each containing 'username', 'email', and 'password'.
        session (AsyncSession): The SQLAlchemy async session.

    Returns:
        list[int]: List of IDs for the newly created users.

    Example:
        users = [
            {"username": "michael_brown", "email": "michael.brown@example.com", "password": "pass1234"},
            {"username": "sarah_wilson", "email": "sarah.wilson@example.com", "password": "mysecurepwd"},
            ...
        ]
        run(create_user_example_4(users_data=users))
    """

    users_list = [
        User(
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"],
        )
        for user_data in users_data
    ]

    session.add_all(users_list)

    await session.commit()  # Commit to persist all users at once

    return [user.id for user in users_list]


users = [
    {
        "username": "michael_brown",
        "email": "michael.brown@example.com",
        "password": "pass1234",
    },
    {
        "username": "sarah_wilson",
        "email": "sarah.wilson@example.com",
        "password": "mysecurepwd",
    },
    {
        "username": "david_clark",
        "email": "david.clark@example.com",
        "password": "davidsafe123",
    },
    {
        "username": "emma_walker",
        "email": "emma.walker@example.com",
        "password": "walker987",
    },
    {
        "username": "james_martin",
        "email": "james.martin@example.com",
        "password": "martinpass001",
    },
]

run(create_user_example_4(users_data=users))  # type: ignore
