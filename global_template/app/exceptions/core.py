"""Core exception handling utilities for the application.

This module defines the base exception class for application-specific errors,
as well as the global exception handler for FastAPI. It provides a unified
structure for error reporting, localization, and formatting of error responses.

All exceptions derived from AppBaseException can be localized and will be
returned to the client in a consistent JSON format, including error codes,
messages, and additional context parameters.
"""

import time

from typing import Dict, Any

from fastapi import Request
from fastapi.responses import JSONResponse

from fastapi_babel import _  # type: ignore

from global_template.app.exceptions.models import (
    ErrorResponseModel,
)


class AppBaseException(Exception):
    """
    Base class for all application-specific exceptions.

    This exception class provides a standard structure for error handling
    throughout the application. It supports localization of error messages
    using a message key and optional parameters, and defines a consistent
    error code and HTTP status code for each exception type.

    Attributes:
        status_code (int): HTTP status code to return (default: 500).
        error_code (str): Internal error code for programmatic identification.
        message_key (str): Localization key for the error message.
        message_params (dict): Parameters for formatting the localized message.
    """

    status_code: int = 500
    error_code: str = "app_error"
    message_key: str = "errors.app.general"
    message_params: Dict[str, Any] = {}

    def __init__(
        self,
        message_key: str | None = None,
        message_params: Dict[str, Any] | None = None,
    ):
        """
        Initialize the exception with an optional message key and parameters.

        Args:
            message_key (str, optional): Override the default localization key.
            message_params (dict, optional): Parameters for message formatting.
        """

        self.message_key = message_key or self.message_key
        self.message_params = message_params or {}

        # Call the base Exception constructor with the message key for logging/debugging.
        super().__init__(self.message_key)

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize the exception details to a dictionary.

        Returns:
            dict: A dictionary containing the error code, message key, and parameters.
        """

        return {
            "error_code": self.error_code,
            "message_key": self.message_key,
            "message_params": self.message_params,
        }


async def app_exception_handler(
    _request: Request, exc: Exception
) -> JSONResponse:
    """
    FastAPI exception handler for application-specific exceptions.

    This handler intercepts exceptions derived from AppBaseException,
    localizes the error message, and returns a structured JSON response
    to the client. It also measures and includes the time taken to handle
    the error in the response headers for debugging and performance monitoring.

    Args:
        _request (Request): The incoming HTTP request (unused).
        exc (Exception): The exception that was raised.

    Returns:
        JSONResponse: A JSON response with error details and appropriate status code.

    Raises:
        exc: If the exception is not an AppBaseException, it is re-raised.
    """

    if isinstance(exc, AppBaseException):
        start = time.perf_counter()

        # Localize and format the error message using the provided key and parameters.
        message = _(exc.message_key).format(**exc.message_params)

        # Create a structured error response model.
        error_response = ErrorResponseModel(
            status_code=exc.status_code,
            message=message,
            error_code=exc.error_code,
        )

        end = time.perf_counter()

        elapsed = end - start

        # Return the error response as JSON, including the error handling time in headers.
        return JSONResponse(
            content=error_response.model_dump(),
            status_code=exc.status_code,
            headers={"X-ErrorHandleTime": f"{elapsed:.6f}"},
        )

    # If the exception is not handled here, propagate it further.
    raise exc
