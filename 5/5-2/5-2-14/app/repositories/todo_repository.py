"""Repository for ToDo model."""

from app.db.models import ToDo
from app.repositories.base_repository import Repository


class ToDoRepository(Repository):
    """
    Repository for ToDo model.

    Provides CRUD operations for ToDo items using the base Repository.
    """

    model = ToDo
