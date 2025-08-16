"""DOC"""

from fastapi import HTTPException, status

from sqlalchemy.exc import IntegrityError

from global_template.app.api.schemas.userprofile import (
    UserProfileCreate,
    UserProfileFromDB,
    UserProfileUpdate,
)
from global_template.app.utils.unitofwork import IUnitOfWork
from global_template.app.exceptions.userprofile_exceptions import (
    UserProfileNotFoundError,
    UserProfileIntegrityError,
)
from global_template.app.exceptions.db_exceptions import (
    DBException,
)


class UserProfileService:
    """DOC"""

    def __init__(self, uow: IUnitOfWork):
        """DOC"""

        self.uow = uow

    async def create_profile(
        self, profile_create: UserProfileCreate
    ) -> UserProfileFromDB:
        """DOC"""

        profile_data: dict = profile_create.model_dump()

        try:
            async with self.uow:
                profile_db = await self.uow.userprofile.add_one(profile_data)

                await self.uow.commit()

                return UserProfileFromDB.model_validate(profile_db)
        except IntegrityError as e:
            raise UserProfileIntegrityError(
                message_key="userprofile.create.integrity_error",
                message_params={"user_id": profile_data.get("user_id")},
            ) from e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create user profile: {e}",
            ) from e

    async def get_all_profiles(self) -> list[UserProfileFromDB]:
        """DOC"""

        async with self.uow:
            profiles = await self.uow.userprofile.get_all()

            return [UserProfileFromDB.model_validate(p) for p in profiles]

    async def get_profile_by_id(self, profile_id: int) -> UserProfileFromDB:
        """DOC"""

        async with self.uow:
            profile = await self.uow.userprofile.get_by_id(profile_id)

            if not profile:
                raise UserProfileNotFoundError(
                    message_params={"profile_id": profile_id}
                )

            return UserProfileFromDB.model_validate(profile)

    async def update_profile(
        self, profile_id: int, profile_update: UserProfileUpdate
    ) -> UserProfileFromDB:
        """DOC"""

        update_data = {
            k: v
            for k, v in profile_update.model_dump().items()
            if v is not None
        }

        if not update_data:
            return await self.get_profile_by_id(profile_id)

        try:
            async with self.uow:
                profile = await self.uow.userprofile.get_by_id(profile_id)

                if not profile:
                    raise UserProfileNotFoundError(
                        message_params={"profile_id": profile_id}
                    )

                await self.uow.userprofile.update(profile_id, update_data)
                await self.uow.commit()

                profile = await self.uow.userprofile.get_by_id(profile_id)

                return UserProfileFromDB.model_validate(profile)
        except IntegrityError as e:
            raise UserProfileIntegrityError(
                message_key="profile.update.integrity_error",
                message_params={"profile_id": profile_id},
            ) from e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update profile: {e}",
            ) from e

    async def delete_profile(self, profile_id: int) -> None:
        """DOC"""

        async with self.uow:
            profile = await self.uow.userprofile.get_by_id(profile_id)

            if not profile:
                raise UserProfileNotFoundError(
                    message_params={"profile_id": profile_id}
                )

            deleted = await self.uow.userprofile.delete(profile_id)

            if not deleted:
                raise DBException(
                    message_key="errors.userprofile.delete_failed",
                    message_params={"profile_id": profile_id},
                )

            await self.uow.commit()
