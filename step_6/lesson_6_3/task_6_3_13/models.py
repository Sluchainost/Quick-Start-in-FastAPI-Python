"""Models for user registration, user data, and error responses."""

from pydantic import BaseModel, EmailStr


class UserRegistrationModel(BaseModel):
    """
    Model for user registration request.
    """

    name: str
    email: EmailStr


class UserModel(BaseModel):
    """
    Model representing a user in the system.
    """

    id: int
    name: str
    email: EmailStr


class ErrorResponseModel(BaseModel):
    """
    Model for standardized error responses.
    """

    status_code: int
    message: str
    error_code: str | int
