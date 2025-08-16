"""DOC"""

from typing import Dict, Any

from global_template.app.exceptions.core import AppBaseException


class ToDoException(AppBaseException):
    """DOC"""

    status_code: int = 500
    error_code: str = "todo_error"
    message_key: str = "errors.todo.general"

    def __init__(
        self,
        message_key: str | None = None,
        message_params: Dict[str, Any] | None = None,
    ):

        super().__init__(
            message_key=message_key or self.message_key,
            message_params=message_params,
        )


class ToDoNotFoundError(ToDoException):
    """DOC"""

    status_code: int = 404
    error_code: str = "todo_not_found"
    message_key: str = "errors.todo.not_found"


class ToDoAlreadyExistsError(ToDoException):
    """DOC"""

    status_code: int = 409
    error_code: str = "todo_already_exists"
    message_key: str = "errors.todo.already_exists"


class ToDoValidationError(ToDoException):
    """DOC"""

    status_code: int = 422
    error_code: str = "todo_validation_error"
    message_key: str = "errors.todo.validation_error"


class ToDoIntegrityError(ToDoException):
    """DOC"""

    status_code: int = 400
    error_code: str = "todo_integrity_error"
    message_key: str = "errors.todo.integrity_error"
