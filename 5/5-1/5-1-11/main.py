"""Main entry point for the FastAPI application.

This module initializes the FastAPI app, includes the necessary routers, and
starts the application using Uvicorn when executed as the main module.
This design allows for easy development with live reloading.
"""

import uvicorn

from fastapi import FastAPI

from app.api.endpoints.todo import todo_router


app = FastAPI()

app.include_router(todo_router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
