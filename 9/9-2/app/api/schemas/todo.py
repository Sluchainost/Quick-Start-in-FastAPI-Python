""" DOC """

import datetime

from pydantic import BaseModel


class ToDoCreate(BaseModel):
    """ DOC """

    description: str
    completed: bool | None = False


class ToDoFromDB(ToDoCreate):
    """ DOC """

    id: int
    created_at: datetime.datetime
