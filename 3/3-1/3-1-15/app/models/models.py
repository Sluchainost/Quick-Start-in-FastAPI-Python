""" Module for creating a Pydantic model """

from pydantic import BaseModel, EmailStr, PositiveInt, Field


class UserCreate(BaseModel):
    """ Pydantic model """

    name: str
    email: EmailStr
    age: PositiveInt | None = Field(default=None, lt=130)
    is_subscribed: bool = False
