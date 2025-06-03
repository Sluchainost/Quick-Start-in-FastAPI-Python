"""This module defines the Product ORM model for the SQLAlchemy database.

The Product class represents a product entity in the database, with fields for
title, price, count, and description. This model inherits from the Base class,
which provides common fields such as id, created_at, and updated_at.

This file is intended as an educational example for learning about SQLAlchemy
ORM models and Alembic migrations.
"""

from sqlalchemy import text

from sqlalchemy.types import String
from sqlalchemy.orm import Mapped, mapped_column

from step_5.lesson_5_3.task_5_3_14.database import Base


class Product(Base):
    """
    ORM model representing a product in the database.

    Attributes:
        title (str): The name/title of the product (max 50 characters, required).
        price (int): The price of the product in integer units (required).
        count (int): The available quantity of the product in stock (required).
        description (str): A textual description of the product (required, defaults to 'Default description').
    """

    title: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    count: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(
        nullable=False, server_default=text("'Default description'")
    )
