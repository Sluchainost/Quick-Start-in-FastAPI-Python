"""DOC"""

from fastapi import HTTPException, status

from sqlalchemy.exc import IntegrityError

from global_template.app.api.schemas.tag import (
    TagCreate,
    TagFromDB,
    TagUpdate,
)
from global_template.app.utils.unitofwork import IUnitOfWork
from global_template.app.exceptions.tag_exceptions import (
    TagNotFoundError,
    TagIntegrityError,
)
from global_template.app.exceptions.db_exceptions import (
    DBException,
)


class TagService:
    """DOC"""

    def __init__(self, uow: IUnitOfWork):
        """DOC"""

        self.uow = uow

    async def create_tag(self, tag_create: TagCreate) -> TagFromDB:
        """DOC"""

        tag_data: dict = tag_create.model_dump()

        try:
            async with self.uow:
                tag_db = await self.uow.tag.add_one(tag_data)

                await self.uow.commit()

                return TagFromDB.model_validate(tag_db)
        except IntegrityError as e:
            raise TagIntegrityError(
                message_key="tag.create.integrity_error",
                message_params={"name": tag_data.get("name")},
            ) from e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create tag: {e}",
            ) from e

    async def get_all_tags(self) -> list[TagFromDB]:
        """DOC"""

        async with self.uow:
            tags = await self.uow.tag.get_all()

            return [TagFromDB.model_validate(t) for t in tags]

    async def get_tag_by_id(self, tag_id: int) -> TagFromDB:
        """DOC"""

        async with self.uow:
            tag = await self.uow.tag.get_by_id(tag_id)

            if not tag:
                raise TagNotFoundError(message_params={"tag_id": tag_id})

            return TagFromDB.model_validate(tag)

    async def update_tag(
        self, tag_id: int, tag_update: TagUpdate
    ) -> TagFromDB:
        """DOC"""

        update_data = {
            k: v for k, v in tag_update.model_dump().items() if v is not None
        }

        if not update_data:
            return await self.get_tag_by_id(tag_id)

        try:
            async with self.uow:
                tag = await self.uow.tag.get_by_id(tag_id)

                if not tag:
                    raise TagNotFoundError(message_params={"tag_id": tag_id})

                await self.uow.tag.update(tag_id, update_data)
                await self.uow.commit()

                tag = await self.uow.tag.get_by_id(tag_id)

                return TagFromDB.model_validate(tag)
        except IntegrityError as e:
            raise TagIntegrityError(
                message_key="tag.update.integrity_error",
                message_params={"tag": tag_id},
            ) from e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update tag: {e}",
            ) from e

    async def delete_tag(self, tag_id: int) -> None:
        """DOC"""

        async with self.uow:
            tag = await self.uow.tag.get_by_id(tag_id)

            if not tag:
                raise TagNotFoundError(message_params={"tag_id": tag_id})

            deleted = await self.uow.tag.delete(tag_id)

            if not deleted:
                raise DBException(message_key="errors.tag.delete_failed")

            await self.uow.commit()
