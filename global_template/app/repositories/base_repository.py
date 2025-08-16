"""DOC"""

from typing import Any, Generic, TypeVar, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update as sa_update, delete as sa_delete

from global_template.app.db.database import Base


ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """DOC"""

    def __init__(self, session: AsyncSession, model: type[ModelType]):
        """DOC"""

        self.session = session
        self.model = model

    async def add_one(self, obj_data: dict) -> ModelType:
        """DOC"""

        obj = self.model(**obj_data)
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def get_all(self) -> Sequence[ModelType]:
        """DOC"""

        q = select(self.model)
        result = await self.session.execute(q)
        return result.scalars().all()

    async def get_by_id(self, obj_id: Any) -> ModelType | None:
        """DOC"""

        q = select(self.model).where(self.model.id == obj_id)
        result = await self.session.execute(q)
        return result.scalars().first()

    async def update(self, obj_id: Any, update_data: dict) -> None:
        """DOC"""

        q = (
            sa_update(self.model)
            .where(self.model.id == obj_id)
            .values(**update_data)
            .execution_options(synchronize_session="fetch")
        )
        await self.session.execute(q)

    async def delete(self, obj_id: Any) -> bool:
        """DOC"""

        q = sa_delete(self.model).where(self.model.id == obj_id)
        result = await self.session.execute(q)
        return result.rowcount > 0
