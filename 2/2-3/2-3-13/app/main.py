"""A module that provides a server for efficient operation of applications."""

import uvicorn

from fastapi import FastAPI

from models.models import Feedback


app = FastAPI()

lst = []


@app.post('/feedback')
async def feedback_message(feedback: Feedback):
    """ add feedback in 'database' and return it """

    lst.append({"name": feedback.name, "feedback": feedback.message})
    return {"message": f"Feedback received. Thank you, {feedback.name}!"}


@app.get("/comments")
async def show_feedback():
    """ return all comment from 'database' """

    return lst


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
