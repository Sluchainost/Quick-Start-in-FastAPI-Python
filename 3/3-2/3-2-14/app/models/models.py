""" Module for creating a Pydantic model for users. """

from pydantic import BaseModel


class User(BaseModel):
    """ Pydantic model """

    username: str
    password: str
