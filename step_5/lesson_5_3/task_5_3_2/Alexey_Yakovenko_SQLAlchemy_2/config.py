"""
This module manages project configuration using Pydantic's BaseSettings.

Features:
- Loads database connection settings from a .env file for reproducibility and security.
- Provides a method to construct the SQLAlchemy async database URL.
- Ensures all configuration is type-checked and easily extendable for scientific workflows.

Usage:
    from config import settings
    db_url = settings.get_db_url()
"""

import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Loads and validates environment variables for database configuration.

    Attributes:
        DB_HOST (str): Database server hostname or IP address.
        DB_PORT (int): Database server port.
        DB_USER (str): Database username.
        DB_PASS (str): Database password.
        DB_NAME (str): Name of the target database.

    The configuration is loaded from a .env file located in the same directory as this script.
    """

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    # Specify the .env file location for loading environment variables.
    model_config = SettingsConfigDict(
        env_file=os.path.join(
            os.path.dirname(os.path.abspath(__file__)), ".env"
        )
    )

    def get_db_url(self):
        """
        Constructs the SQLAlchemy async database URL using the loaded settings.

        Returns:
            str: The database URL in the format required by SQLAlchemy with asyncpg driver.
        """

        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


# Instantiate the settings object for use throughout the project.
settings = Settings()
