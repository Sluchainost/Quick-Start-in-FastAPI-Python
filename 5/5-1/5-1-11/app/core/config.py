"""Configuration module for application settings.

This module loads and validates environment variables required
for database connectivity.
"""

import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for application configuration.

    Attributes:
        DB_HOST (str): The hostname of the database server.
        DB_PORT (str): The port number for the database server.
        DB_USER (str): The username for database authentication.
        DB_PASS (str): The password for database authentication.
        DB_NAME (str): The name of the database.
    """

    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def async_database_url(self):
        """Constructs the asynchronous database URL.

        Returns:
            str: A database URL formatted for use with asyncpg and SQLAlchemy.
        """

        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        """Configuration for Pydantic Settings.

        Attributes:
            env_file (str): Path to the .env file containing
                            environment variables.
        """

        env_file = os.path.join(os.path.dirname(__file__), '../../.env')


settings = Settings()
