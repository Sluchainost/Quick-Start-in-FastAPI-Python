"""A module that provides a server for efficient operation of applications."""


import uvicorn

from fastapi import FastAPI, HTTPException

from models.models import UserCreate


app = FastAPI()
users: list[UserCreate] = []


@app.post('/create_user')
async def create_user(new_user: UserCreate) -> UserCreate:
    """ processes incoming user data """

    # Check for duplicate email
    if any(user.email == new_user.email for user in users):
        raise HTTPException(status_code=400,
                            detail="Email already registered.")

    users.append(new_user)
    return new_user


@app.get('/showuser')
async def show_users():
    """ show all users data """

    return {"users": users}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
