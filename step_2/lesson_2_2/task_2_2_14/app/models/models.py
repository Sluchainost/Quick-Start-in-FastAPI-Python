""" Module for creating a Pydantic model """

from pydantic import BaseModel


class User(BaseModel):
    """ Pydantic model """

    name: str
    age: int
    is_adult: bool = False
