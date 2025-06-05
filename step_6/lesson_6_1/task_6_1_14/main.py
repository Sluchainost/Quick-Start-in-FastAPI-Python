"""Main entry point for the FastAPI application with custom exception handling."""

import uvicorn

from fastapi import FastAPI

from step_6.lesson_6_1.task_6_1_14.endpoints import main_router
from step_6.lesson_6_1.task_6_1_14.exceptions import (
    CustomExceptionA,
    CustomExceptionB,
    custom_exception_a_handler,
    custom_exception_b_handler,
    global_exception_handler,
)


app = FastAPI(
    title="FastAPI Custom Exception Demo",
    description="An educational example of custom exceptions and handlers in FastAPI.",
    version="1.0.0",
)

app.include_router(main_router)

# Register exception handlers on the app
app.add_exception_handler(CustomExceptionA, custom_exception_a_handler)
app.add_exception_handler(CustomExceptionB, custom_exception_b_handler)
app.add_exception_handler(Exception, global_exception_handler)


if __name__ == "__main__":
    uvicorn.run(
        app="step_6.lesson_6_1.task_6_1_14.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
