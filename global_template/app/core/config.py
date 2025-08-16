"""Configuration module for application settings.

This module loads and validates environment variables required
for database connectivity and authentication. It uses Pydantic's
BaseSettings to provide type validation and automatic loading
from a .env file or system environment variables.

This file is intended as a template for robust, maintainable
application configuration management.
"""

import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Settings for application configuration.

    This class defines all environment-based configuration options
    for the application, including database connection parameters
    and JWT authentication settings.

    Attributes:
        DB_HOST (str): The hostname of the database server.
        DB_PORT (str): The port number for the database server.
        DB_USER (str): The username for database authentication.
        DB_PASS (str): The password for database authentication.
        DB_NAME (str): The name of the database.
        JWT_SECRET_KEY (str): Secret key used for JWT token signing.
        JWT_ALGORITHM (str): Algorithm used for JWT encoding/decoding.
        ACCESS_TOKEN_EXPIRE_MINUTES (int): Token expiration time in minutes.
    """

    DB_HOST: (
        str  # Database server hostname (e.g., "localhost" or "db.example.com")
    )
    DB_PORT: str  # Database server port (e.g., "5432" for PostgreSQL)
    DB_USER: str  # Username for authenticating with the database
    DB_PASS: str  # Password for authenticating with the database
    DB_NAME: str  # Name of the database to connect to

    JWT_SECRET_KEY: str  # Secret key for signing JWT tokens
    JWT_ALGORITHM: str = "HS256"  # Default JWT signing algorithm
    ACCESS_TOKEN_EXPIRE_MINUTES: int = (
        60 * 24
    )  # Default token expiration (24 hours)

    @property
    def async_database_url(self):
        """
        Constructs the asynchronous database URL.

        This property builds a SQLAlchemy-compatible database URL
        for use with asyncpg (asynchronous PostgreSQL driver).

        Returns:
            str: A database URL formatted for use with asyncpg and SQLAlchemy.

        Example:
            postgresql+asyncpg://user:password@host:port/dbname
        """

        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        """
        Configuration for Pydantic Settings.

        This inner class tells Pydantic where to look for environment
        variables. By default, it loads from a .env file located two
        directories above this file, but system environment variables
        will override values in the .env file.

        Attributes:
            env_file (str): Path to the .env file containing
                            environment variables.
        """

        env_file = os.path.join(os.path.dirname(__file__), "../../.env")


# Instantiate the settings object at import time.
# This makes configuration available throughout the application.
settings = Settings()  # type: ignore
