"""FastAPI app for user authentication and protected resource management."""

import uvicorn

from fastapi import FastAPI, HTTPException, Depends, status

from dependencies import get_user, get_user_from_token, create_jwt_token

from models.models import UserSchema


app = FastAPI()


@app.post("/login")
async def login(user_in: UserSchema):
    """Authenticate user and return JWT token.

    Args:
        user_in (UserSchema): User credentials with username and password.

    Returns:
        dict: Contains JWT access token if authentication successful.

    Raises:
        HTTPException: 401 error if password is invalid.
    """

    user = get_user(user_in.username)

    if user.password != user_in.password:
        raise HTTPException(
            detail='The password provided is an invalid password',
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    return {
        "access_token": create_jwt_token(
            {"sub": user_in.username}
        ),
        # "token_type": "bearer"
    }


@app.get("/protected_resource")
async def about_me(current_user: str = Depends(get_user_from_token)):
    """Retrieve user information from protected endpoint.

    Args:
        current_user (str): Username extracted from JWT token.

    Returns:
        User: User object containing user information.

    Raises:
        HTTPException: 401 error if credentials are invalid.
    """

    user = get_user(current_user)

    if not user:
        raise HTTPException(
            detail="Invalid credentials",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    return user


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
