"""A module that provides a server for efficient operation of applications."""

import uvicorn

from fastapi import FastAPI

from models.models import User


app = FastAPI()


@app.post('/user')
async def check_user_age(user: User):
    """ return valid user """

    if user.age >= 18:
        user.is_adult = True
    return user


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
