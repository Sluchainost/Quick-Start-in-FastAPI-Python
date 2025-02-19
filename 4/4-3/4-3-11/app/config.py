"""Application configuration and environment settings.

This module defines configuration constants used throughout the application
for JWT token generation, encryption, and session management.

Note:
    In production, sensitive values should be loaded from environment
    variables or secure configuration management systems.
"""


SECRET_KEY: str = "mysecretkey"
ALGORITHM: str = "HS256"
EXPIRATION_TIME_SECONDS: int = 30
