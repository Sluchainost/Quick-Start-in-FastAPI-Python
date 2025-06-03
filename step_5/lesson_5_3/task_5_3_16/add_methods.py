"""This module provides a utility function to insert mock Product data into the database.

It demonstrates how to bulk-insert product records using SQLAlchemy ORM, including
setting the product status via an enumeration. Intended for educational purposes
to illustrate batch insertion, ORM session management, and enum usage.
"""

from step_5.lesson_5_3.task_5_3_16.models import Product
from step_5.lesson_5_3.task_5_3_16.database import session
from step_5.lesson_5_3.task_5_3_16.sql_enums import ProductStatus


def insert_mock_data(products_data: list[dict]) -> list[int]:
    """
    Insert a list of product records into the database.

    Args:
        products_data (list[dict]): A list of dictionaries, each containing product fields:
            - title (str): The product's title.
            - price (int): The product's price.
            - count (int): The available quantity.
            - description (str or None): The product's description (can be None for default).
            - status (str): The product's status (should match ProductStatus values).

    Returns:
        list[int]: A list of IDs of the newly inserted products.
    """

    # Create Product ORM instances from the input data
    products_list = [
        Product(
            title=product_data["title"],
            price=product_data["price"],
            count=product_data["count"],
            description=product_data["description"],
            status=product_data["status"],
        )
        for product_data in products_data
    ]

    # Add all new products to the session
    session.add_all(products_list)

    # Commit the transaction to persist changes and assign IDs
    session.commit()

    # Return the list of new product IDs
    return [product.id for product in products_list]


# Example product data to be inserted, using ProductStatus enum values
products = [
    {
        "title": "apple",
        "price": 20,
        "count": 5,
        "description": None,
        "status": ProductStatus.ARCHIVED.value,
    },
    {
        "title": "potato",
        "price": 10,
        "count": 15,
        "description": None,
        "status": ProductStatus.DEPRECATED.value,
    },
]

# Insert the mock products and retrieve their IDs
products_ids = insert_mock_data(products)

# Print confirmation for each inserted product
for product_id in products_ids:
    print(f"Add product with ID {product_id}")
