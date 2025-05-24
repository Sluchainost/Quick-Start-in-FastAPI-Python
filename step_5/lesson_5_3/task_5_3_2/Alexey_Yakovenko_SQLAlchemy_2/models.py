"""
This module defines the core SQLAlchemy ORM models for the scientific project:
User, Profile, Post, and Comment.

Each model inherits from the project's declarative Base and is designed for
asynchronous database interaction. All relationships, field types, and constraints
are explicitly documented for scientific clarity and reproducibility.
"""

from sqlalchemy import ForeignKey, text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .dao.database import Base, uniq_str_an, array_or_none_an, content_an

from .sql_enums import GenderEnum, ProfessionEnum, StatusPost, RatingEnum


class Profile(Base):
    """
    Represents a user's profile, containing personal and professional information.

    Attributes:
        first_name (str): The user's first name (required).
        last_name (str | None): The user's last name (optional).
        age (int | None): The user's age (optional).
        gender (GenderEnum): The user's gender (required, enumerated).
        profession (ProfessionEnum): The user's profession (default: DEVELOPER, DB default: UNEMPLOYED).
        interests (List[str] | None): List of user's interests (optional).
        contacts (dict | None): Arbitrary contact information, stored as JSON (optional).
        user_id (int): Foreign key referencing the associated User (unique, one-to-one).
        user (User): Relationship to the User model (back_populates 'profile').
    """

    first_name: Mapped[str]
    last_name: Mapped[str | None]
    age: Mapped[int | None]
    gender: Mapped[GenderEnum]
    profession: Mapped[ProfessionEnum] = mapped_column(
        default=ProfessionEnum.DEVELOPER, server_default=text("'UNEMPLOYED'")
    )
    interests: Mapped[array_or_none_an]
    contacts: Mapped[dict | None] = mapped_column(JSON)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)

    # One-to-one relationship: each profile belongs to exactly one user.
    user: Mapped["User"] = relationship(
        "User", back_populates="profile", uselist=False
    )


class User(Base):
    """
    Represents a user account in the system.

    Attributes:
        username (str): Unique username for authentication.
        email (str): Unique email address.
        password (str): Hashed password for authentication.
        profile (Profile): One-to-one relationship to the user's profile.
        posts (List[Post]): One-to-many relationship to the user's posts.
        comments (List[Comment]): One-to-many relationship to the user's comments.
    """

    username: Mapped[uniq_str_an]
    email: Mapped[uniq_str_an]
    password: Mapped[str]

    # One-to-one relationship: each user has a single profile.
    profile: Mapped["Profile"] = relationship(
        "Profile",
        back_populates="user",
        uselist=False,
        lazy="joined",  # Eagerly loads the profile when querying a user.
    )

    # One-to-many: a user can have multiple posts.
    posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="user",
        cascade="all, delete-orphan",  # Deleting a user deletes their posts.
    )

    # One-to-many: a user can have multiple comments.
    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="user",
        cascade="all, delete-orphan",  # Deleting a user deletes their comments.
    )


class Post(Base):
    """
    Represents a post created by a user.

    Attributes:
        title (str): Title of the post.
        content (str): Main textual content of the post.
        main_photo_url (str): URL to the main photo for the post.
        photos_url (List[str] | None): List of URLs to additional photos (optional).
        status (StatusPost): Publication status (default: PUBLISHED, DB default: DRAFT).
        user_id (int): Foreign key referencing the authoring user.
        user (User): Relationship to the User model (back_populates 'posts').
        comments (List[Comment]): One-to-many relationship to comments on this post.
    """

    title: Mapped[str]
    content: Mapped[content_an]
    main_photo_url: Mapped[str]
    photos_url: Mapped[array_or_none_an]
    status: Mapped[StatusPost] = mapped_column(
        default=StatusPost.PUBLISHED,
        server_default=text("'DRAFT'"),
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # Many-to-one: each post is authored by a single user.
    user: Mapped["User"] = relationship("User", back_populates="posts")

    # One-to-many: a post can have multiple comments.
    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="post",
        cascade="all, delete-orphan",  # Deleting a post deletes its comments.
    )


class Comment(Base):
    """
    Represents a comment made by a user on a post.

    Attributes:
        content (str): The textual content of the comment.
        user_id (int): Foreign key referencing the commenting user.
        post_id (int): Foreign key referencing the post being commented on.
        is_published (bool): Whether the comment is published (default: True, DB default: false).
        rating (RatingEnum): Rating associated with the comment (default: FIVE, DB default: SEVEN).
        user (User): Relationship to the User model (back_populates 'comments').
        post (Post): Relationship to the Post model (back_populates 'comments').
    """

    content: Mapped[content_an]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    is_published: Mapped[bool] = mapped_column(
        default=True, server_default=text("'false'")
    )
    rating: Mapped[RatingEnum] = mapped_column(
        default=RatingEnum.FIVE, server_default=text("'SEVEN'")
    )

    # Many-to-one: each comment is authored by a single user.
    user: Mapped["User"] = relationship("User", back_populates="comments")

    # Many-to-one: each comment belongs to a single post.
    post: Mapped["Post"] = relationship("Post", back_populates="comments")
