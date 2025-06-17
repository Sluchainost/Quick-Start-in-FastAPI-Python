"""Main entry point for the User API FastAPI application with i18n support."""

import uvicorn

from fastapi import FastAPI

from fastapi_babel import Babel, BabelConfigs, BabelMiddleware  # type: ignore

from step_6.lesson_6_3.task_6_3_13.endpoints import router
from step_6.lesson_6_3.task_6_3_13.exceptions import (
    user_not_found_exception_handler,
    invalid_user_data_exception_handler,
    UserNotFoundException,
    InvalidUserDataException,
)


app = FastAPI(
    title="User API",
    description="A sample FastAPI application demonstrating custom error handling and internationalization.",
    version="1.0.0",
)

# Initialize Babel for i18n
babel_configs = BabelConfigs(
    ROOT_DIR=__file__,
    BABEL_DEFAULT_LOCALE="en",
    BABEL_TRANSLATION_DIRECTORY="locales",
)

# Initialize the Babel object using the configuration
babel = Babel(configs=babel_configs)

app.add_middleware(BabelMiddleware, babel_configs=babel_configs)

# Register custom exception handlers
app.add_exception_handler(
    UserNotFoundException, user_not_found_exception_handler
)
app.add_exception_handler(
    InvalidUserDataException, invalid_user_data_exception_handler
)

# Include API router
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(
        app="step_6.lesson_6_3.task_6_3_13.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
