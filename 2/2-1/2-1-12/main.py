"""A module that provides a server for efficient operation of applications."""

import uvicorn

from fastapi import FastAPI
from fastapi.responses import FileResponse


app = FastAPI()


@app.get("/")
async def root():
    """returns html page"""

    return FileResponse('2/2-1/2-1-12/index.html')

# @app.get("/", response_class=FileResponse)
# async def root_html():
#     """return html page"""
#
#     return '2/2-1/2-1-12/index.html'


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
