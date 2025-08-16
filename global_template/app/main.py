"""Main entry point for the FastAPI application.

This module initializes the FastAPI app, includes the necessary routers, and
starts the application using Uvicorn when executed as the main module.
This design allows for easy development with live reloading.
"""

import uvicorn

from fastapi import FastAPI

from fastapi_babel import Babel, BabelConfigs, BabelMiddleware  # type: ignore

from global_template.app.api.endpoints.todo import todo_router
from global_template.app.api.endpoints.user import user_router
from global_template.app.api.endpoints.tag import tag_router
from global_template.app.api.endpoints.userprofile import (
    userprofile_router,
)

from global_template.app.exceptions.core import (
    AppBaseException,
    app_exception_handler,
)

app = FastAPI()

# Initialize Babel for i18n
babel_configs = BabelConfigs(
    ROOT_DIR=__file__,
    BABEL_DEFAULT_LOCALE="en",
    BABEL_TRANSLATION_DIRECTORY="global_template/app/i18n",
)

# Initialize the Babel object using the configuration
babel = Babel(configs=babel_configs)

app.add_middleware(BabelMiddleware, babel_configs=babel_configs)

app.add_exception_handler(AppBaseException, app_exception_handler)

app.include_router(todo_router)
app.include_router(user_router)
app.include_router(tag_router)
app.include_router(userprofile_router)

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
