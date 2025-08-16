"""ORM models for the ToDo application.

This module defines the SQLAlchemy ORM models representing users, user profiles,
to-do items, tags, and their relationships. The models are designed for use with
an async SQLAlchemy engine and inherit from a custom Base class that provides
common fields and conventions.

Each model includes detailed documentation and comments to serve as a learning
template for best practices in ORM modeling.
"""

from sqlalchemy import Boolean, ForeignKey, String, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from global_template.app.db.database import Base


# Association table for the many-to-many relationship between ToDo and Tag.
# Each row links a ToDo item to a Tag.
todo_tag_association = Table(
    "todo_tag_association",
    Base.metadata,
    Column("todo_id", ForeignKey("todos.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)


class User(Base):
    """
    ORM model representing an application user.

    Attributes:
        id (int): Primary key, inherited from Base.
        username (str): Unique username for the user.
        email (str): Unique email address for the user.
        todos (list[ToDo]): List of to-do items created by the user.
        profile (UserProfile): One-to-one relationship to the user's profile.
        created_at (datetime): Timestamp when the user was created (from Base).
        updated_at (datetime): Timestamp when the user was last updated (from Base).
    """

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        doc="Unique username for the user (max 50 characters).",
    )
    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        doc="Unique email address for the user (max 100 characters).",
    )

    # One-to-many relationship: a user can have multiple to-do items.
    todos: Mapped[list["ToDo"]] = relationship(
        "ToDo",
        back_populates="user",
        cascade="all, delete-orphan",
        doc="List of to-do items created by the user.",
    )

    # One-to-one relationship: each user has a single profile.
    profile: Mapped["UserProfile"] = relationship(
        "UserProfile",
        uselist=False,
        back_populates="user",
        cascade="all, delete-orphan",
        doc="One-to-one relationship to the user's profile.",
    )


class UserProfile(Base):
    """
    ORM model representing additional profile information for a user.

    Attributes:
        id (int): Primary key, inherited from Base.
        user_id (int): Foreign key referencing the associated user.
        bio (str | None): Optional biography or description.
        avatar_url (str | None): Optional URL to the user's avatar image.
        user (User): The user to whom this profile belongs.
        created_at (datetime): Timestamp when the profile was created (from Base).
        updated_at (datetime): Timestamp when the profile was last updated (from Base).
    """

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
        doc="Foreign key referencing the associated user (unique, one-to-one).",
    )
    bio: Mapped[str | None] = mapped_column(
        String(250),
        nullable=True,
        doc="Optional biography or description (max 250 characters).",
    )
    avatar_url: Mapped[str | None] = mapped_column(
        String(250),
        nullable=True,
        doc="Optional URL to the user's avatar image (max 250 characters).",
    )

    # Relationship back to the User; uselist=False ensures one-to-one.
    user: Mapped[User] = relationship(
        "User",
        back_populates="profile",
        doc="The user to whom this profile belongs.",
    )


class ToDo(Base):
    """
    ORM model representing a to-do item.

    Attributes:
        id (int): Primary key, inherited from Base.
        title (str): Title of the to-do item.
        description (str | None): Optional detailed description.
        completed (bool): Completion status of the to-do item.
        user_id (int): Foreign key referencing the creator (User).
        user (User): The user who created this to-do item.
        tags (list[Tag]): List of tags associated with this to-do item.
        created_at (datetime): Timestamp when the to-do was created (from Base).
        updated_at (datetime): Timestamp when the to-do was last updated (from Base).
    """

    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        doc="Title of the to-do item (max 100 characters).",
    )
    description: Mapped[str | None] = mapped_column(
        String(250),
        nullable=True,
        doc="Optional detailed description of the to-do item (max 250 characters).",
    )
    completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        doc="Completion status of the to-do item (default: False).",
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        doc="Foreign key referencing the user who created this to-do item.",
    )

    # Relationship to the User who owns this to-do item.
    user: Mapped[User] = relationship(
        "User",
        back_populates="todos",
        doc="The user who created this to-do item.",
    )

    # Many-to-many relationship: a to-do item can have multiple tags.
    tags: Mapped[list["Tag"]] = relationship(
        "Tag",
        secondary=todo_tag_association,
        back_populates="todos",
        doc="List of tags associated with this to-do item.",
    )


class Tag(Base):
    """
    ORM model representing a tag for categorizing to-do items.

    Attributes:
        id (int): Primary key, inherited from Base.
        name (str): Unique name of the tag.
        todos (list[ToDo]): List of to-do items associated with this tag.
        created_at (datetime): Timestamp when the tag was created (from Base).
        updated_at (datetime): Timestamp when the tag was last updated (from Base).
    """

    name: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        doc="Unique name of the tag (max 30 characters).",
    )

    # Many-to-many relationship: a tag can be associated with multiple to-do items.
    todos: Mapped[list[ToDo]] = relationship(
        "ToDo",
        secondary=todo_tag_association,
        back_populates="tags",
        doc="List of to-do items associated with this tag.",
    )
