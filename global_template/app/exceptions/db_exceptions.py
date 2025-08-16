"""
Database Exception Classes

This module defines a hierarchy of exception classes for handling database-related errors
within the application. Each exception class corresponds to a specific type of database error,
providing a consistent structure for error reporting, localization, and HTTP status codes.

All database exceptions inherit from `DBException`, which itself extends the core
`AppBaseException`. This design allows for centralized error handling and easy extension
for new database error types as needed.

Usage:
    Raise these exceptions in your data access layer or repository code to signal
    specific database error conditions to the application layer.
"""

from typing import Dict, Any

from global_template.app.exceptions.core import AppBaseException


class DBException(AppBaseException):
    """
    Base exception for all database-related errors.

    This class serves as the parent for all specific database exceptions.
    It sets a default error code, message key, and HTTP status code for
    general database errors. Subclasses should override these attributes
    to provide more specific error information.

    Attributes:
        status_code (int): HTTP status code to return (default: 500).
        error_code (str): Internal error code for identifying the error type.
        message_key (str): Localization key for the error message.
    """

    status_code: int = 500
    error_code: str = "db_error"
    message_key: str = "errors.db.general"

    def __init__(
        self,
        message_key: str | None = None,
        message_params: Dict[str, Any] | None = None,
    ):
        """
        Initialize the database exception.

        Args:
            message_key (str, optional): Override the default localization key.
            message_params (dict, optional): Parameters for formatting the localized message.
        """

        # Pass the resolved message key and parameters to the base exception.
        super().__init__(
            message_key=message_key or self.message_key,
            message_params=message_params,
        )


class DBConnectionError(DBException):
    """
    Exception raised when a database connection cannot be established.

    This error typically indicates that the database server is unreachable,
    credentials are invalid, or there is a network issue.

    Attributes:
        status_code (int): HTTP status code 503 (Service Unavailable).
        error_code (str): "db_connection_error".
        message_key (str): "errors.db.connection_error".
    """

    status_code: int = 503
    error_code: str = "db_connection_error"
    message_key: str = "errors.db.connection_error"


class DBRecordNotFound(DBException):
    """
    Exception raised when a requested database record does not exist.

    Use this exception when a query for a specific record (by ID or unique key)
    returns no results.

    Attributes:
        status_code (int): HTTP status code 404 (Not Found).
        error_code (str): "db_record_not_found".
        message_key (str): "errors.db.record_not_found".
    """

    status_code: int = 404
    error_code: str = "db_record_not_found"
    message_key: str = "errors.db.record_not_found"


class DBAlreadyExistsError(DBException):
    """
    Exception raised when attempting to create a record that already exists.

    Use this exception when a unique constraint is violated, such as trying to
    insert a duplicate primary key or unique field.

    Attributes:
        status_code (int): HTTP status code 409 (Conflict).
        error_code (str): "db_already_exists".
        message_key (str): "errors.db.already_exists".
    """

    status_code: int = 409
    error_code: str = "db_already_exists"
    message_key: str = "errors.db.already_exists"


class DBValidationError(DBException):
    """
    Exception raised when data provided for a database operation is invalid.

    This error should be used when input data fails validation checks before
    being persisted to the database (e.g., missing required fields, invalid formats).

    Attributes:
        status_code (int): HTTP status code 422 (Unprocessable Entity).
        error_code (str): "db_validation_error".
        message_key (str): "errors.db.validation_error".
    """

    status_code: int = 422
    error_code: str = "db_validation_error"
    message_key: str = "errors.db.validation_error"


class DBIntegrityError(DBException):
    """
    Exception raised when a database integrity constraint is violated.

    This includes foreign key violations, check constraints, or other relational
    integrity errors that occur during database operations.

    Attributes:
        status_code (int): HTTP status code 400 (Bad Request).
        error_code (str): "db_integrity_error".
        message_key (str): "errors.db.integrity_error".
    """

    status_code: int = 400
    error_code: str = "db_integrity_error"
    message_key: str = "errors.db.integrity_error"
