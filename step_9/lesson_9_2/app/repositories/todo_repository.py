"""This module provides the repository implementation for ToDo items.
It extends the base repository class to interact with
the ToDo ORM model, providing access to persistence
methods such as adding and retrieving ToDo records.
"""

from app.db.models import ToDo
from app.repositories.base_repository import Repository


class ToDoRepository(Repository):
    """Repository for managing ToDo items in the data store.

    This repository extends the base Repository to handle operations specific
    to ToDo items. It configures the model attribute to use the ToDo ORM model,
    allowing for CRUD operations tailored to the ToDo entity.
    """

    model = ToDo
