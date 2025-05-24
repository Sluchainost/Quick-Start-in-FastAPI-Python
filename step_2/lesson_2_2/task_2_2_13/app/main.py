"""A module that provides a server for efficient operation of applications."""

import uvicorn

from fastapi import FastAPI

from models.models import User


user = User(name='John Doe', id=1)
app = FastAPI()


@app.get("/users", response_model=User)
async def user_root():
    """ return Pydantic model """

    return user


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
