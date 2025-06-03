"""This module defines the Product ORM model for the database.

The Product class represents a product entity with fields for title, price, count,
description, and status. The status field uses a custom enumeration for product state.
This model is intended for use with SQLAlchemy and supports default values and
server-side defaults for certain fields.
"""

from sqlalchemy import text

from sqlalchemy.types import String
from sqlalchemy.orm import Mapped, mapped_column

from step_5.lesson_5_3.task_5_3_15.database import Base
from step_5.lesson_5_3.task_5_3_15.sql_enums import ProductStatus


class Product(Base):
    """
    ORM model representing a product in the database.

    Attributes:
        title (str): The name/title of the product (max 50 characters, required).
        price (int): The price of the product (required).
        count (int): The available quantity of the product in stock (required).
        description (str): A textual description of the product (required, defaults to 'Default description').
        status (ProductStatus): The status of the product (enum, defaults to DRAFT).
    """

    title: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    count: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(
        nullable=False, server_default=text("'Default description'")
    )
    status: Mapped[ProductStatus] = mapped_column(
        default=ProductStatus.DRAFT, server_default=text("'DRAFT'")
    )
