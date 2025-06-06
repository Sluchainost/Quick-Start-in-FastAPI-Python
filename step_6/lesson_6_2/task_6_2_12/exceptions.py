"""Custom exception handlers for FastAPI application.

This module contains custom exception handlers to provide
user-friendly error responses for specific types of exceptions,
such as validation errors. These handlers can be registered
with the FastAPI application to override the default error
responses and improve the API's usability and clarity.

Functions:
    validation_exception_handler: Handles Pydantic validation errors
        and returns a structured JSON response.
"""

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def validation_exception_handler(
    request: Request,  # pylint: disable=unused-argument
    exc: RequestValidationError,
) -> JSONResponse:
    """
    Handle Pydantic validation errors and return a custom JSON response.

    Args:
        request (Request): The HTTP request object that caused the validation error.
        exc (RequestValidationError): The exception instance containing validation details.

    Returns:
        JSONResponse: A JSON response with status code 422 and details about the validation errors.
    """

    # Construct a JSON response with a custom message and the list of validation errors.
    return JSONResponse(
        status_code=422,
        content={
            "message": "Invalid input",
            "errors": exc.errors(),  # List of validation error details
        },
    )
