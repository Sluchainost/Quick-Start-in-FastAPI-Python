"""DOC"""

from step_5.lesson_5_3.task_5_3_14.models import Product
from step_5.lesson_5_3.task_5_3_14.database import session


def insert_mock_data(products_data: list[dict]) -> list[int]:
    """DOC"""

    products_list = [
        Product(
            title=product_data["title"],
            price=product_data["price"],
            count=product_data["count"],
            description=product_data["description"],
        )
        for product_data in products_data
    ]

    session.add_all(products_list)

    session.commit()

    return [product.id for product in products_list]


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

products_ids = insert_mock_data(products)

for product_id in products_ids:
    print(f"Add product with ID {product_id}")
