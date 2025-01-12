""" Module for creating a Pydantic model for products. """

from pydantic import BaseModel


class Product(BaseModel):
    """ Pydantic model """

    product_id: int
    name: str
    category: str
    price: float
