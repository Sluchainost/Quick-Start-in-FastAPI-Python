"""DOC"""

from fastapi import HTTPException, status

from sqlalchemy.exc import IntegrityError

from global_template.app.utils.unitofwork import IUnitOfWork
from global_template.app.api.schemas.user import (
    UserCreate,
    UserFromDB,
    UserUpdate,
)
from global_template.app.exceptions.user_exceptions import (
    UserNotFoundError,
    UserIntegrityError,
    UserAlreadyExistsError,
)
from global_template.app.exceptions.db_exceptions import (
    DBException,
)


class UserService:
    """DOC"""

    def __init__(self, uow: IUnitOfWork):
        """DOC"""

        self.uow = uow

    async def create_user(self, user_create: UserCreate) -> UserFromDB:
        """DOC"""

        user_data: dict = user_create.model_dump()

        existing_user = await self.uow.user.get_by_email(
            user_data.get("email")
        )
        if existing_user is not None:
            raise UserAlreadyExistsError(
                message_params={"email": user_data.get("email")}
            )

        try:
            async with self.uow:
                user_db = await self.uow.user.add_one(user_data)

                await self.uow.commit()

                return UserFromDB.model_validate(user_db)
        except IntegrityError as e:
            raise UserIntegrityError(
                message_key="user.create.integrity_error",
                message_params={"email": user_data.get("email")},
            ) from e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create user: {e}",
            ) from e

    async def get_all_users(self) -> list[UserFromDB]:
        """DOC"""

        async with self.uow:
            users = await self.uow.user.get_all()

            return [UserFromDB.model_validate(u) for u in users]

    async def get_user_by_id(self, user_id: int) -> UserFromDB:
        """DOC"""

        async with self.uow:
            user = await self.uow.user.get_by_id(user_id)

            if not user:
                raise UserNotFoundError(message_params={"user_id": user_id})

            return UserFromDB.model_validate(user)

    async def update_user(
        self, user_id: int, user_update: UserUpdate
    ) -> UserFromDB:
        """DOC"""

        update_data = {
            k: v for k, v in user_update.model_dump().items() if v is not None
        }

        if not update_data:
            return await self.get_user_by_id(user_id)

        try:
            async with self.uow:
                user = await self.uow.user.get_by_id(user_id)

                if not user:
                    raise UserNotFoundError(
                        message_params={"user_id": user_id}
                    )

                await self.uow.user.update(user_id, update_data)
                await self.uow.commit()

                user = await self.uow.user.get_by_id(user_id)

                return UserFromDB.model_validate(user)
        except IntegrityError as e:
            raise UserIntegrityError(
                message_key="user.update.integrity_error",
                message_params={"user_id": user_id},
            ) from e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update user: {e}",
            ) from e

    async def delete_user(self, user_id: int) -> None:
        """DOC"""

        async with self.uow:
            user = await self.uow.user.get_by_id(user_id)

            if not user:
                raise UserNotFoundError(message_params={"user_id": user_id})

            deleted = await self.uow.user.delete(user_id)

            if not deleted:
                raise DBException(
                    message_key="errors.user.delete_failed",
                    message_params={"user_id": user_id},
                )

            await self.uow.commit()
