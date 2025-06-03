"""Configuration module for application settings using Pydantic BaseSettings.

This module defines the Settings class, which loads database configuration
from environment variables or a .env file. It provides a method to construct
the database URL for SQLAlchemy or other database clients.

Intended for use in educational examples demonstrating environment-based
configuration management with Pydantic.
"""

import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or a .env file.

    Attributes:
        DB_HOST (str): Database host address.
        DB_PORT (str): Database port number.
        DB_USER (str): Database username.
        DB_NAME (str): Database name.
        DB_PASS (str): Database password.
    """

    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_NAME: str
    DB_PASS: str

    # Specify the .env file location for loading environment variables
    model_config = SettingsConfigDict(
        env_file=os.path.join(
            os.path.dirname(os.path.abspath(__file__)), ".env"
        )
    )

    def get_db_url(self):
        """
        Construct the PostgreSQL database URL from the settings.

        Returns:
            str: The database connection URL in SQLAlchemy format.
        """

        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASS}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


# Instantiate the settings object for use throughout the application
settings = Settings()
