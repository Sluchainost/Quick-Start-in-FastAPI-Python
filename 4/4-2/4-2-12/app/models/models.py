"""User schema module defining data models for authentication."""

from pydantic import BaseModel


class UserSchema(BaseModel):
    """User authentication model with username and password fields."""

    username: str
    password: str
