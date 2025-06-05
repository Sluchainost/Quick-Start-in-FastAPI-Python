"""Custom exception classes and handlers for FastAPI application."""

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from step_6.lesson_6_1.task_6_1_14.models import (
    CustomExceptionAModel,
    CustomExceptionBModel,
)


class CustomExceptionA(HTTPException):
    """
    Custom exception for resource not found or similar errors (e.g., 404).
    """

    def __init__(
        self, *, status_code: int, message: str, detail: str | None = None
    ):
        """
        :param status_code: HTTP status code to return.
        :param message: Short description of the error.
        :param detail: Additional details about the error.
        """

        super().__init__(status_code=status_code, detail=detail)
        self.message = message


class CustomExceptionB(HTTPException):
    """
    Custom exception for forbidden access or similar errors (e.g., 403).
    """

    def __init__(
        self, *, status_code: int, message: str, detail: str | None = None
    ):
        """
        :param status_code: HTTP status code to return.
        :param message: Short description of the error.
        :param detail: Additional details about the error.
        """

        super().__init__(status_code=status_code, detail=detail)
        self.message = message


async def custom_exception_a_handler(
    request: Request, exc: Exception  # pylint: disable=unused-argument
) -> JSONResponse:
    """
    Exception handler for CustomExceptionA.
    Returns a structured JSON error response using CustomExceptionAModel.
    """

    # Defensive: check type before accessing custom attributes
    if not isinstance(exc, CustomExceptionA):

        # fallback for unexpected usage
        return JSONResponse(
            status_code=500, content={"error": "Internal server error"}
        )

    print(
        f"[CustomExceptionA] {exc.status_code}: {exc.message} | {exc.detail}"
    )

    error = jsonable_encoder(
        CustomExceptionAModel(
            status_code=exc.status_code,
            er_message=exc.message,
            er_details=exc.detail,
        )
    )

    return JSONResponse(status_code=exc.status_code, content=error)


async def custom_exception_b_handler(
    request: Request, exc: Exception  # pylint: disable=unused-argument
) -> JSONResponse:
    """
    Exception handler for CustomExceptionB.
    Returns a structured JSON error response using CustomExceptionBModel.
    """

    if not isinstance(exc, CustomExceptionB):

        return JSONResponse(
            status_code=500, content={"error": "Internal server error"}
        )

    print(
        f"[CustomExceptionB] {exc.status_code}: {exc.message} | {exc.detail}"
    )

    error = jsonable_encoder(
        CustomExceptionBModel(
            status_code=exc.status_code,
            er_message=exc.message,
            er_details=exc.detail,
        )
    )

    return JSONResponse(status_code=exc.status_code, content=error)


async def global_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:  # pylint: disable=unused-argument
    """
    Global exception handler for uncaught exceptions.
    Returns a generic 500 Internal Server Error response.
    """

    print(f"[GlobalException] {type(exc).__name__}: {exc}")

    return JSONResponse(
        status_code=500, content={"error": "Internal server error"}
    )
