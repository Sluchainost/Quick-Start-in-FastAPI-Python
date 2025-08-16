"""DOC"""

from typing import Dict, Any

from global_template.app.exceptions.core import AppBaseException


class UserException(AppBaseException):
    """DOC"""

    status_code: int = 500
    error_code: str = "user_error"
    message_key: str = "errors.user.general"

    def __init__(
        self,
        message_key: str | None = None,
        message_params: Dict[str, Any] | None = None,
    ):

        super().__init__(
            message_key=message_key or self.message_key,
            message_params=message_params,
        )


class UserNotFoundError(UserException):
    """DOC"""

    status_code: int = 404
    error_code: str = "user_not_found"
    message_key: str = "errors.user.not_found"


class UserAlreadyExistsError(UserException):
    """DOC"""

    status_code: int = 409
    error_code: str = "user_already_exists"
    message_key: str = "errors.user.already_exists"


class UserValidationError(UserException):
    """DOC"""

    status_code: int = 422
    error_code: str = "user_validation_error"
    message_key: str = "errors.user.validation_error"


class UserIntegrityError(UserException):
    """DOC"""

    status_code: int = 400
    error_code: str = "user_integrity_error"
    message_key: str = "errors.user.integrity_error"
