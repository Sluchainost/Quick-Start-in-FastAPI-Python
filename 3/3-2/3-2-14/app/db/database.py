""" fake database """

from models.models import User


sample_user: dict = {"username": "user123", "password": "password123"}
fake_db: list[User] = [User(**sample_user)]
