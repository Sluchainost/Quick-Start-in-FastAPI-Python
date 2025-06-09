"""Custom exceptions and exception handlers for user-related errorswith i18n support."""

import time

from fastapi import Request

from fastapi.responses import JSONResponse

from step_6.lesson_6_3.task_6_3_13.models import ErrorResponseModel


class UserNotFoundException(Exception):
    """
    Exception raised when a user is not found in the database.
    """

    def __init__(self, status_code: int, message: str, error_code: str | int):

        self.status_code = status_code
        self.message = message
        self.error_code = error_code


class InvalidUserDataException(Exception):
    """
    Exception raised when user registration data is invalid.
    """

    def __init__(self, status_code: int, message: str, error_code: str | int):

        self.status_code = status_code
        self.message = message
        self.error_code = error_code


async def user_not_found_exception_handler(
    _request: Request, exc: Exception
) -> JSONResponse:
    """
    Exception handler for UserNotFoundException.
    Returns a standardized error response with processing time header.
    """

    if isinstance(exc, UserNotFoundException):

        start = time.perf_counter()

        error_response = ErrorResponseModel(
            status_code=exc.status_code,
            message=exc.message,
            error_code=exc.error_code,
        )

        end = time.perf_counter()
        elapsed = end - start

        return JSONResponse(
            content=error_response.model_dump(),
            status_code=exc.status_code,
            headers={"X-ErrorHandleTime": f"{elapsed:.6f}"},
        )

    raise exc


async def invalid_user_data_exception_handler(
    _request: Request, exc: Exception
) -> JSONResponse:
    """
    Exception handler for InvalidUserDataException.
    Returns a standardized error response with processing time header.
    """

    if isinstance(exc, InvalidUserDataException):

        start = time.perf_counter()

        error_response = ErrorResponseModel(
            status_code=exc.status_code,
            message=exc.message,
            error_code=exc.error_code,
        )

        end = time.perf_counter()
        elapsed = end - start

        return JSONResponse(
            content=error_response.model_dump(),
            status_code=exc.status_code,
            headers={"X-ErrorHandleTime": f"{elapsed:.6f}"},
        )

    raise exc
