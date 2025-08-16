"""DOC"""

from typing import Dict, Any

from global_template.app.exceptions.core import AppBaseException


class UserProfileException(AppBaseException):
    """DOC"""

    status_code: int = 500
    error_code: str = "userprofile_error"
    message_key: str = "errors.userprofile.general"

    def __init__(
        self,
        message_key: str | None = None,
        message_params: Dict[str, Any] | None = None,
    ):

        super().__init__(
            message_key=message_key or self.message_key,
            message_params=message_params,
        )


class UserProfileNotFoundError(UserProfileException):
    """DOC"""

    status_code: int = 404
    error_code: str = "userprofile_not_found"
    message_key: str = "errors.userprofile.not_found"


class UserProfileAlreadyExistsError(UserProfileException):
    """DOC"""

    status_code: int = 409
    error_code: str = "userprofile_already_exists"
    message_key: str = "errors.userprofile.already_exists"


class UserProfileValidationError(UserProfileException):
    """DOC"""

    status_code: int = 422
    error_code: str = "userprofile_validation_error"
    message_key: str = "errors.userprofile.validation_error"


class UserProfileIntegrityError(UserProfileException):
    """DOC"""

    status_code: int = 400
    error_code: str = "userprofile_integrity_error"
    message_key: str = "errors.userprofile.integrity_error"
