""" FastAPI application for header validation.

This module implements a REST API endpoint that validates HTTP headers,
specifically the User-Agent and Accept-Language headers, ensuring they
meet specified format requirements.
"""

from typing import Annotated

import uvicorn

from fastapi import FastAPI, Header, HTTPException


app = FastAPI()


@app.get("/headers")
def root(user_agent: Annotated[str | None, Header()] = None,
         accept_language: Annotated[str | None, Header()] = None):
    """ Validate and return User-Agent and Accept-Language headers.

    Args:
        user_agent (str | None): The User-Agent header from the request.
        accept_language (str | None): The Accept-Language header from the
            request.

    Returns:
        dict: A dictionary containing the validated headers:
            {
                "User-Agent": str,
                "Accept-Language": str
            }

    Raises:
        HTTPException:
            - 400 if either header is missing
            - 400 if Accept-Language format is invalid

    Note:
        Accept-Language must exactly match: "en-US,en;q=0.9,es;q=0.8"
    """

    if user_agent is None or accept_language is None:
        raise HTTPException(
            status_code=400,
            detail='Must be User-Agent and Accept-Language'
        )
    if accept_language != "en-US,en;q=0.9,es;q=0.8":
        raise HTTPException(
            status_code=400,
            detail='Accept-Language is bad format'
        )

    return {
        "User-Agent": user_agent,
        "Accept-Language": accept_language
    }


if __name__ == "__main__":
    uvicorn.run("solution_2:app", host="127.0.0.1", port=8000, reload=True)
