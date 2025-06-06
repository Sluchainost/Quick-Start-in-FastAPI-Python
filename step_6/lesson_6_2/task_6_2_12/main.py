"""Main application entry point for FastAPI.

This module initializes the FastAPI application, registers custom
exception handlers, and includes API routers. It serves as the
starting point for running the web server.

Usage:
    Run this file to start the FastAPI application.
"""

import uvicorn

from fastapi import FastAPI

from step_6.lesson_6_2.task_6_2_12.endpoints import router
from step_6.lesson_6_2.task_6_2_12.exceptions import (
    validation_exception_handler,
    RequestValidationError,
)


app = FastAPI(
    title="FastAPI Custom Exception Demo",
    description="An educational example of custom exceptions and handlers in FastAPI.",
    version="1.0.0",
)

# Include the API router containing endpoint definitions.
app.include_router(router)

# Register a custom exception handler for validation errors.
# This handler will be called whenever a RequestValidationError is raised,
# providing a user-friendly error response.
app.add_exception_handler(
    RequestValidationError, validation_exception_handler  # type: ignore[arg-type]
)


if __name__ == "__main__":
    uvicorn.run(
        app="step_6.lesson_6_2.task_6_2_12.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
