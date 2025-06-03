"""Product ORM model definition for the database.

This module defines the Product class, which represents a product entity in the database.
The Product model includes fields for title, price, count, description, status, and is_featured.
- The 'status' field uses a custom enumeration (ProductStatus) to represent the product's state.
- The 'description' field uses the SQLAlchemy Text type for longer text content.
- The 'is_featured' field is a boolean indicating whether the product is featured.

Intended for use with SQLAlchemy ORM and supports default values and server-side defaults.
"""

from sqlalchemy import text, Boolean, false, Text

from sqlalchemy.types import String
from sqlalchemy.orm import Mapped, mapped_column

from step_5.lesson_5_3.task_5_3_16.database import Base
from step_5.lesson_5_3.task_5_3_16.sql_enums import ProductStatus


class Product(Base):
    """
    ORM model representing a product in the database.

    Attributes:
        title (str): The name/title of the product (max 50 characters, required).
        price (int): The price of the product (required).
        count (int): The available quantity of the product in stock (required).
        description (str): A textual description of the product (required, defaults to 'Default description').
            Uses the SQLAlchemy Text type for potentially long content.
        status (ProductStatus): The status of the product (enum, defaults to DRAFT).
        is_featured (bool): Indicates whether the product is featured (defaults to False).
    """

    title: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    count: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(
        Text, nullable=False, server_default=text("'Default description'")
    )
    status: Mapped[ProductStatus] = mapped_column(
        default=ProductStatus.DRAFT, server_default=text("'DRAFT'")
    )
    is_featured: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=false()
    )
