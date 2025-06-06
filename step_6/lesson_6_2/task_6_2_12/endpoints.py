"""API endpoints for FastAPI application.

This module defines the HTTP endpoints (routes) for the FastAPI application.
Each endpoint is associated with a specific HTTP method and path, and
performs actions such as creating or retrieving resources.

Functions:
    create_user: Handles POST requests to create a new user with validated data.
"""

from fastapi import APIRouter

from step_6.lesson_6_2.task_6_2_12.models import User


router = APIRouter()


@router.post("/items/", response_model=User, status_code=201)
async def user_data(user: User):
    """
    Create a new user.

    This endpoint receives a JSON payload representing user data,
    validates it using the User Pydantic model, and returns the
    created user data in the response.

    Args:
        user (User): The user data parsed and validated from the request body.

    Returns:
        User: The created user data as a JSON response.
    """

    # In a real application, you would save the user to a database here.
    # For this educational example, we simply return the validated user data.

    return user
