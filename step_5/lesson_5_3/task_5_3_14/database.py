"""DOC"""

from datetime import datetime

from sqlalchemy import Integer, func, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    declared_attr,
    sessionmaker,
)

from step_5.lesson_5_3.task_5_3_14.config import settings


DATABASE_URL = settings.get_db_url()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


class Base(DeclarativeBase):
    """DOC"""

    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),  # pylint: disable=not-callable
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),  # pylint: disable=not-callable,
        onupdate=func.now(),  # pylint: disable=not-callable,
    )

    @classmethod
    @declared_attr.directive
    def __tablename__(cls) -> str:
        """DOC"""

        return cls.__name__.lower() + "s"
