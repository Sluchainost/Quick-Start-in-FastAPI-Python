""" FastAPI application for validating and processing HTTP headers.
This module provides functionality to validate and handle HTTP headers,
specifically User-Agent and Accept-Language headers, through a REST API.
"""

import re

import uvicorn

from fastapi import FastAPI, HTTPException, Request


app = FastAPI()


def check_headers(headers: Request.headers):
    """ Validate the presence and format of required HTTP headers.

    Args:
        headers (Request.headers): The HTTP request headers to validate.

    Raises:
        HTTPException:
            - 400 status code if User-Agent header is missing
            - 400 status code if Accept-Language header is missing
            - 400 status code if Accept-Language header format is invalid

    The Accept-Language header must follow the format:
    - Can contain language codes (2-5 characters) or '*'
    - Optional quality value (;q=0.0 to ;q=1.0)
    - Multiple values separated by commas
    Example: "en-US,en;q=0.9,es;q=0.8"
    """

    if "User-Agent" not in headers:
        raise HTTPException(status_code=400,
                            detail="The User-Agent header not found!")

    if "Accept-Language" not in headers:
        raise HTTPException(status_code=400,
                            detail="The Accept-Language header not found!")

    pattern = (
        r"(?i:(?:\*|[a-z\-]{2,5})(?:;q=\d\.\d)?,"
        r")+(?:\*|[a-z\-]{2,5})(?:;q=\d\.\d)?"
               )

    if not re.fullmatch(pattern, headers["Accept-Language"]):
        raise HTTPException(
            status_code=400,
            detail="The Accept-Language header is not in the correct format"
        )


@app.get("/headers")
async def get_headers(request: Request) -> dict:
    """ Retrieve and validate User-Agent and Accept-Language headers.

    Args:
        request (Request): The incoming HTTP request object.

    Returns:
        dict: A dictionary containing the validated headers.
            Format: {
                "User-Agent": "<user-agent-string>",
                "Accept-Language": "<accept-language-string>"
            }

    Raises:
        HTTPException: If header validation fails (see check_headers function).
    """

    check_headers(request.headers)

    return {
        "User-Agent": request.headers["user-agent"],
        "Accept-Language": request.headers["accept-language"]
    }


if __name__ == "__main__":
    uvicorn.run("solution_1:app", host="127.0.0.1", port=8000, reload=True)
