"""Main entry point for the FastAPI application.

This module initializes the FastAPI app and registers the todo endpoint router.
It serves as the starting point for the application when run directly.
In a development environment, uvicorn is used to start the ASGI server
with automatic reload on code changes.
"""

import uvicorn

from fastapi import FastAPI

from app.api.endpoints.todo import todo_router


# Create an instance of the FastAPI application.
app = FastAPI()

# Include the router for todo endpoints to register API routes.
app.include_router(todo_router)


if __name__ == "__main__":
    # Run the application with uvicorn on localhost:8000
    # with reload enabled for development.
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
