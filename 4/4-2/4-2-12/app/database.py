"""Mock database module containing user data for authentication testing."""

from models.models import UserSchema


USERS_DATA = [
    UserSchema(**{"username": "Tor", "password": "tor"}),
    UserSchema(**{"username": "Loki", "password": "loki"})
]
