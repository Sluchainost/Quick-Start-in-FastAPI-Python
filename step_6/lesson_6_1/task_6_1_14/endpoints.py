"""FastAPI endpoints demonstrating custom exception handling."""

from fastapi import APIRouter, status

from step_6.lesson_6_1.task_6_1_14.exceptions import (
    CustomExceptionA,
    CustomExceptionB,
)
from step_6.lesson_6_1.task_6_1_14.models import (
    CustomExceptionAModel,
    CustomExceptionBModel,
    ItemsResponse,
)


main_router = APIRouter(tags=["Main"])


@main_router.get(
    "/items/{item_id}/",
    response_model=ItemsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Items by ID",
    description="The endpoint returns item_id by ID. If the item_id is 42, an exception with the status code 404 is returned.",
    responses={
        status.HTTP_200_OK: {"model": ItemsResponse},
        status.HTTP_404_NOT_FOUND: {"model": CustomExceptionAModel},
    },
)
async def read_item(item_id: int):
    """
    Retrieve an item by its ID.
    Raises CustomExceptionA if the item_id is 42 (simulating not found).
    """

    if item_id == 42:
        raise CustomExceptionA(
            status_code=404,
            message="You are trying to access an item that does not exist.",
            detail="Item with this ID was not found.",
        )
    return ItemsResponse(item_id=item_id)


@main_router.get(
    "/secret/",
    response_model=None,
    status_code=status.HTTP_200_OK,
    summary="Access secret resource",
    description="If the user is not 'admin', raises CustomExceptionB (403 Forbidden).",
    responses={
        status.HTTP_200_OK: {"description": "Access granted"},
        status.HTTP_403_FORBIDDEN: {
            "model": CustomExceptionBModel,
            "description": "Access forbidden",
        },
    },
)
async def secret_area(user: str = "guest"):
    """
    Access a secret resource.
    Raises CustomExceptionB if the user is not 'admin'.
    """
    if user != "admin":
        raise CustomExceptionB(
            status_code=403,
            message="Access forbidden.",
            detail=f"User '{user}' does not have access to this resource.",
        )
    return {"message": "Welcome to the secret area, admin!"}
