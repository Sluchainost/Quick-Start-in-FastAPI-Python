"""Module for creating a Pydantic model"""

from pydantic import BaseModel


class User(BaseModel):
    """Pydantic model"""

    name: str
    id: int
