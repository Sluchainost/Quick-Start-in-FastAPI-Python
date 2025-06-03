"""This module provides utility functions for inserting mock product data into the database.

It defines a function to bulk-insert product records using SQLAlchemy ORM and demonstrates
its usage with example product data. Intended for educational purposes to illustrate
batch insertion and ORM session management.
"""

from step_5.lesson_5_3.task_5_3_14.models import Product
from step_5.lesson_5_3.task_5_3_14.database import session


def insert_mock_data(products_data: list[dict]) -> list[int]:
    """
    Insert a list of product records into the database.

    Args:
        products_data (list[dict]): A list of dictionaries, each containing product fields:
            - title (str): The product's title.
            - price (int): The product's price.
            - count (int): The available quantity.
            - description (str): The product's description.

    Returns:
        list[int]: A list of IDs of the newly inserted products.
    """

    products_list = [
        Product(
            title=product_data["title"],
            price=product_data["price"],
            count=product_data["count"],
            description=product_data["description"],
        )
        for product_data in products_data
    ]

    # Add all new products to the session
    session.add_all(products_list)

    # Commit the transaction to persist changes and assign IDs
    session.commit()

    # Return the list of new product IDs
    return [product.id for product in products_list]


# Example product data to be inserted
products = [
    {
        "title": "apple2",
        "price": 20,
        "count": 5,
        "description": "some description1",
    },
    {
        "title": "potato2",
        "price": 10,
        "count": 15,
        "description": "some description2",
    },
]

# Insert the mock products and retrieve their IDs
products_ids = insert_mock_data(products)

# Print confirmation for each inserted product
for product_id in products_ids:
    print(f"Add product with ID {product_id}")
