"""DOC"""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from global_template.app.db.models import User
from global_template.app.repositories.base_repository import (
    BaseRepository,
)


class UserRepository(BaseRepository[User]):
    """DOC"""

    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

    async def get_by_email(self, obj_email: Any) -> User | None:
        """DOC"""

        q = select(self.model).where(self.model.email == obj_email)

        result = await self.session.execute(q)

        return result.scalars().first()
