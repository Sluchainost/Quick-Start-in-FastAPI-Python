""" DOC """

from sqlalchemy.ext.asyncio import (async_sessionmaker, create_async_engine,
                                    AsyncSession)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


engine = create_async_engine(settings.async_database_url)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    """ DOC """

    async with async_session_maker() as session:
        yield session


class Base(DeclarativeBase):
    """ DOC """
