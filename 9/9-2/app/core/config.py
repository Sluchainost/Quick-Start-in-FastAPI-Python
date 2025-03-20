"""This module defines the application configuration settings.
It loads environment variables necessary to connect to the PostgreSQL database
and provides a utility property to construct the asynchronous database URL.
"""

import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Encapsulates environment variables required for configuring
       the database connection and other settings.

    Attributes:
        DB_HOST (str): The hostname of the database server.
        DB_PORT (str): The port number of the database server.
        DB_USER (str): The username for the database connection.
        DB_PASS (str): The password for the database connection.
        DB_NAME (str): The name of the database.
    """

    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def async_database_url(self):
        """Constructs and returns the asynchronous database URL
           for connecting to PostgreSQL.

        The URL is formatted for use with asyncpg by combining
        the provided database settings.

        Returns:
            str: The complete asynchronous database connection URL.
        """

        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            )

    class Config:
        """Pydantic configuration for the Settings class.

        Attributes:
            env_file (str): Specifies the .env file to load
                            environment variables from.
        """

        env_file = os.path.join(os.path.dirname(__file__), '../../.env')


settings = Settings()
