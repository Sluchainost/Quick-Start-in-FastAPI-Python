"""
This module defines Data Access Object (DAO) classes for the main entities in the project:
User, Profile, Post, and Comment. Each DAO provides asynchronous database operations
for its corresponding SQLAlchemy model, leveraging the generic BaseDAO for standard CRUD
and extending with entity-specific logic where needed.

All methods are designed for use with SQLAlchemy's AsyncSession.
"""

from typing import Sequence

from sqlalchemy import select, Row

from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy.ext.asyncio import AsyncSession

from step_5.lesson_5_3.task_5_3_2.Alexey_Yakovenko_SQLAlchemy_2.dao.base import (
    BaseDAO,
)

from step_5.lesson_5_3.task_5_3_2.Alexey_Yakovenko_SQLAlchemy_2.models import (
    User,
    Profile,
    Post,
    Comment,
)


class UserDAO(BaseDAO):
    """
    DAO for the User model.

    Provides both generic CRUD operations (via BaseDAO) and custom methods
    for user creation (with profile), retrieval, and update.
    """

    model = User

    @classmethod
    async def add_user_with_profile(
        cls, session: AsyncSession, user_data: dict
    ) -> User:
        """
        Create a new user and their associated profile in a single transaction.

        Args:
            session (AsyncSession): The active SQLAlchemy async session.
            user_data (dict): Dictionary containing user and profile fields.
                Required keys: username, email, password, first_name, gender.
                Optional keys: last_name, age, profession, interests, contacts.

        Returns:
            User: The newly created User instance (with profile relationship populated).

        Raises:
            Exception: If the operation fails, the transaction is rolled back.
        """

        # Create the User instance from provided data.
        user = cls.model(
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"],
        )

        session.add(user)

        await session.flush()  # Assigns user.id

        # Create the Profile instance, linking to the new user's ID
        profile = Profile(
            user_id=user.id,
            first_name=user_data["first_name"],
            last_name=user_data.get("last_name"),
            age=user_data.get("age"),
            gender=user_data["gender"],
            profession=user_data.get("profession"),
            interests=user_data.get("interests"),
            contacts=user_data.get("contacts"),
        )

        session.add(profile)

        await session.commit()  # Commit both user and profile atomically

        return user

    @classmethod
    async def get_all_users(cls, session: AsyncSession) -> Sequence[User]:
        """
        Retrieve all users from the database.

        Args:
            session (AsyncSession): The active SQLAlchemy async session.

        Returns:
            list[User]: List of all User instances.
        """

        query = select(cls.model)

        result = await session.execute(query)

        records = result.scalars().all()

        return records

    @classmethod
    async def get_username_id(
        cls, session: AsyncSession
    ) -> Sequence[Row[tuple[int, str]]]:
        """
        Retrieve all user IDs and usernames.

        Args:
            session (AsyncSession): The active SQLAlchemy async session.

        Returns:
            list[tuple[int, str]]: List of (id, username) tuples for all users.
        """

        query = select(cls.model.id, cls.model.username)

        print(query)  # For debugging: shows the generated SQL query.

        result = await session.execute(query)

        records = result.all()

        return records

    @classmethod
    async def get_user_info(
        cls, session: AsyncSession, user_id: int
    ) -> User | None:
        """
        Retrieve a single user's information by their ID.

        Args:
            session (AsyncSession): The active SQLAlchemy async session.
            user_id (int): The ID of the user to retrieve.

        Returns:
            User | None: The User instance if found, else None.
        """

        query = select(cls.model).filter_by(id=user_id)

        result = await session.execute(query)

        user_info = result.scalar_one_or_none()

        return user_info

    @classmethod
    async def update_username_age_by_id(
        cls, session: AsyncSession, data_id: int, username: str, age: int
    ) -> None:
        """
        Update a user's username and their profile's age by user ID.

        Args:
            session (AsyncSession): The active SQLAlchemy async session.
            data_id (int): The ID of the user to update.
            username (str): The new username.
            age (int): The new age to set in the user's profile.

        Returns:
            None

        Raises:
            Exception: If the user or profile does not exist.
        """

        user = await session.get(cls.model, data_id)

        if user is None or user.profile is None:
            raise SQLAlchemyError("User or profile does not exist")

        # Update the username directly on the User model.
        user.username = username
        # Update the age on the related Profile model.
        user.profile.age = age

        await session.flush()  # Persist changes to the database.


class ProfileDAO(BaseDAO):
    """
    DAO for the Profile model.

    Inherits all CRUD operations from BaseDAO.
    """

    model = Profile


class PostDAO(BaseDAO):
    """
    DAO for the Post model.

    Inherits all CRUD operations from BaseDAO.
    """

    model = Post


class CommentDAO(BaseDAO):
    """
    DAO for the Comment model.

    Inherits all CRUD operations from BaseDAO.
    """

    model = Comment
