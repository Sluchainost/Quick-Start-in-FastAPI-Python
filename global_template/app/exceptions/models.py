"""
Error Response Model Definition

This module defines a reusable Pydantic model for structuring error responses
in API endpoints. By standardizing the error response format, it ensures
consistency across the application and simplifies error handling for both
developers and API consumers.

Typical usage:
    Return an instance of `ErrorResponseModel` from exception handlers or
    anywhere a structured error response is required.

Example:
    {
        "status_code": 404,
        "message": "Record not found",
        "error_code": "db_record_not_found"
    }
"""

from pydantic import BaseModel


class ErrorResponseModel(BaseModel):
    """
    Standardized error response model for API endpoints.

    This model encapsulates the essential information required to describe
    an error in a consistent, machine- and human-readable format.

    Attributes:
        status_code (int): The HTTP status code associated with the error.
            Example: 404 for "Not Found", 500 for "Internal Server Error".
        message (str): A human-readable, localized error message that can be
            displayed to end users or logged for diagnostics.
        error_code (str): An application-specific error code that uniquely
            identifies the type of error.

    Example:
        >>> ErrorResponseModel(
        ...     status_code=404,
        ...     message="Record not found",
        ...     error_code="db_record_not_found"
        ... )
        ErrorResponseModel(status_code=404, message='Record not found', error_code='db_record_not_found')
    """

    status_code: int  # HTTP status code (e.g., 404, 500)
    message: str  # Localized, human-readable error message
    error_code: str  # Internal application error code (string or integer)

    class Config:
        """
        Pydantic configuration for the model.

        The `schema_extra` attribute provides an example that will be included
        in the generated OpenAPI schema and documentation tools such as Swagger UI.
        """

        schema_extra = {
            "example": {
                "status_code": 404,
                "message": "Record not found",
                "error_code": "db_record_not_found",
            }
        }
