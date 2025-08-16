"""
Tag Exception Classes

This module defines a structured hierarchy of exception classes for handling tag-related
errors within the application. Each exception class corresponds to a specific type of tag
error, providing a consistent structure for error reporting, localization, and HTTP status codes.

All tag exceptions inherit from `TagException`, which itself extends the core
`AppBaseException`. This design allows for centralized error handling and easy extension
for new tag error types as needed.

Usage:
    Raise these exceptions in your tag management logic or service layer to signal
    specific tag error conditions to the application layer.
"""

from typing import Dict, Any

from global_template.app.exceptions.core import AppBaseException


class TagException(AppBaseException):
    """
    Base exception for all tag-related errors.

    This class serves as the parent for all specific tag exceptions.
    It sets a default error code, message key, and HTTP status code for
    general tag errors. Subclasses should override these attributes
    to provide more specific error information.

    Attributes:
        status_code (int): HTTP status code to return (default: 500).
        error_code (str): Internal error code for identifying the error type.
        message_key (str): Localization key for the error message.
    """

    status_code: int = 500
    error_code: str = "tag_error"
    message_key: str = "errors.tag.general"

    def __init__(
        self,
        message_key: str | None = None,
        message_params: Dict[str, Any] | None = None,
    ):
        """
        Initialize the tag exception.

        Args:
            message_key (str, optional): Override the default localization key.
            message_params (dict, optional): Parameters for formatting the localized message.
        """

        # Pass the resolved message key and parameters to the base exception.
        super().__init__(
            message_key=message_key or self.message_key,
            message_params=message_params,
        )


class TagNotFoundError(TagException):
    """
    Exception raised when a requested tag does not exist.

    Use this exception when a query for a specific tag (by ID or name)
    returns no results.

    Attributes:
        status_code (int): HTTP status code 404 (Not Found).
        error_code (str): "tag_not_found".
        message_key (str): "errors.tag.not_found".
    """

    status_code: int = 404
    error_code: str = "tag_not_found"
    message_key: str = "errors.tag.not_found"


class TagAlreadyExistsError(TagException):
    """
    Exception raised when attempting to create a tag that already exists.

    Use this exception when a unique constraint is violated, such as trying to
    insert a duplicate tag name.

    Attributes:
        status_code (int): HTTP status code 409 (Conflict).
        error_code (str): "tag_already_exists".
        message_key (str): "errors.tag.already_exists".
    """

    status_code: int = 409
    error_code: str = "tag_already_exists"
    message_key: str = "errors.tag.already_exists"


class TagValidationError(TagException):
    """
    Exception raised when data provided for a tag operation is invalid.

    This error should be used when input data fails validation checks before
    being persisted or processed (e.g., missing required fields, invalid formats).

    Attributes:
        status_code (int): HTTP status code 422 (Unprocessable Entity).
        error_code (str): "tag_validation_error".
        message_key (str): "errors.tag.validation_error".
    """

    status_code: int = 422
    error_code: str = "tag_validation_error"
    message_key: str = "errors.tag.validation_error"


class TagIntegrityError(TagException):
    """
    Exception raised when a tag-related integrity constraint is violated.

    This includes relational integrity errors that occur during tag operations,
    such as foreign key violations or other business rule violations.

    Attributes:
        status_code (int): HTTP status code 400 (Bad Request).
        error_code (str): "tag_integrity_error".
        message_key (str): "errors.tag.integrity_error".
    """

    status_code: int = 400
    error_code: str = "tag_integrity_error"
    message_key: str = "errors.tag.integrity_error"
