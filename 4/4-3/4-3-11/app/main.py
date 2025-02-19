"""FastAPI application entry point and router configuration.

This module initializes the FastAPI application instance and configures
the routing by including the authentication and resource routers.

Note:
    The application runs on localhost:8000 when executed directly.
"""

import uvicorn

from fastapi import FastAPI

from routes.login import auth
from routes.resources import resource


app = FastAPI()
app.include_router(auth)
app.include_router(resource)


if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)
