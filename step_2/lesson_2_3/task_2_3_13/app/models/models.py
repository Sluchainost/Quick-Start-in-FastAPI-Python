""" Module for creating a Pydantic model """

from pydantic import BaseModel


class Feedback(BaseModel):
    """ Pydantic model """

    name: str
    message: str
