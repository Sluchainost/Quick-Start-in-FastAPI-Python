"""Module for ToDo repository.

This module contains the ToDoRepository class which extends the base
Repository to provide database operations specific to the ToDo model.
It encapsulates CRUD functionalities and adheres to the organization's
repository standard, abstracting the direct interaction with the ORM.
"""

from app.db.models import ToDo
from app.repositories.base_repository import Repository


class ToDoRepository(Repository):
    """Concrete repository for ToDo items.

    This class extends the generic Repository implementation and sets the
    model to the ToDo model. It enables performing database operations
    such as add, query, update, and delete on to-do items, ensuring
    consistent handling of ToDo data throughout the application.
    """

    model = ToDo
