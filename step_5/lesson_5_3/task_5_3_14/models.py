"""DOC"""

from sqlalchemy import text

from sqlalchemy.types import String
from sqlalchemy.orm import Mapped, mapped_column

from step_5.lesson_5_3.task_5_3_14.database import Base


class Product(Base):
    """DOC"""

    title: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    count: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(
        nullable=False, server_default=text("'Default description'")
    )
