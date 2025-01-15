"""A module that provides a server for efficient operation of applications."""

import secrets

import uvicorn

from fastapi import FastAPI, Cookie, Response, HTTPException

from models.models import User
from db.database import fake_db


app = FastAPI()

sessions: dict[str, User] = {}  # simulate session storage


@app.post('/login')
def login(user: User, response: Response):
    """  Log in a user and set a session cookie. """

    for person in fake_db:
        if (person.username == user.username and
           person.password == user.password):
            session_token = secrets.token_urlsafe(16)
            sessions[session_token] = user
            response.set_cookie(key="session_token",
                                value=session_token,
                                httponly=True)
            return {"message": "cookies are set"}

    raise HTTPException(status_code=401, detail="Invalid username or password")


@app.get('/user')
def user_info(session_token=Cookie()):
    """ Retrieve user information based on the session cookie. """

    user = sessions.get(session_token)

    if user:
        return user.model_dump()

    raise HTTPException(status_code=403, detail="Unauthorized access")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
