"""Main entrypoint for the FastAPI ToDo application.

This module initializes the FastAPI app, includes the ToDo router,
and starts the Uvicorn server when executed directly.
"""

import uvicorn

from fastapi import FastAPI

from app.api.endpoints.todo import todo_router


app = FastAPI()

app.include_router(todo_router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
