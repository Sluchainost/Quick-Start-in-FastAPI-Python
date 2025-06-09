"""API endpoints for user registration and user data retrieval with i18n support."""

from fastapi import APIRouter, status

from fastapi_babel import _  # type: ignore

from step_6.lesson_6_3.task_6_3_13.models import (
    UserRegistrationModel,
    UserModel,
)

from step_6.lesson_6_3.task_6_3_13.exceptions import (
    InvalidUserDataException,
    UserNotFoundException,
)


router = APIRouter()

# Simulated in-memory user database
fake_users_db: dict[int, dict] = {
    1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
    2: {"id": 2, "name": "Bob", "email": "bob@example.com"},
}


@router.post(
    "/register", response_model=UserModel, status_code=status.HTTP_201_CREATED
)
async def register_user(user: UserRegistrationModel) -> UserModel:
    """
    Register a new user.
    Raises InvalidUserDataException if the email is already registered.
    """

    for u in fake_users_db.values():

        if u["email"] == user.email:
            raise InvalidUserDataException(
                status_code=400,
                message=_("User with this email already exists."),
                error_code="USER_ALREADY_EXISTS",
            )

    new_id = max(fake_users_db.keys(), default=0) + 1

    fake_users_db[new_id] = {
        "id": new_id,
        "name": user.name,
        "email": user.email,
    }

    return UserModel(**fake_users_db[new_id])


@router.get("/users/{user_id}", response_model=UserModel)
async def get_user(user_id: int) -> UserModel:
    """
    Retrieve user data by user ID.
    Raises UserNotFoundException if the user does not exist.
    """

    user = fake_users_db.get(user_id)

    if not user:

        raise UserNotFoundException(
            status_code=404,
            message=_("User with id={user_id} not found.").format(
                user_id=user_id
            ),
            error_code="USER_NOT_FOUND",
        )

    return UserModel(**user)
