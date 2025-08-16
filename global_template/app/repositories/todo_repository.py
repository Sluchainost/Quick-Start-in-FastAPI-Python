"""DOC"""

from sqlalchemy.ext.asyncio import AsyncSession

from global_template.app.db.models import ToDo
from global_template.app.repositories.base_repository import (
    BaseRepository,
)


class ToDoRepository(BaseRepository[ToDo]):
    """DOC"""

    def __init__(self, session: AsyncSession):
        super().__init__(session, ToDo)
