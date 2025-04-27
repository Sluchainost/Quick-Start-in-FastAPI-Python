"""Configuration module for application settings.

This module defines the Settings class, which loads environment variables
for database configuration and provides the async database URL.
"""

import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    This class uses Pydantic's BaseSettings to automatically load and
    validate environment variables required for database connectivity.
    """

    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def async_database_url(self):
        """Construct the asynchronous database URL from environment variables.

        Returns:
            str: The asyncpg-compatible PostgreSQL database URL.
        """

        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        """Configuration for loading environment variables from a file.

        Specifies the path to the .env file containing environment variables.
        """

        env_file = os.path.join(os.path.dirname(__file__), '../../.env')


settings = Settings()
