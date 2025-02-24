""" DOC """

import datetime

from sqlalchemy import BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class ToDo(Base):
    """ DOC """

    __tablename__ = "todo"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    description: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
                                                DateTime,
                                                nullable=False,
                                                default=datetime.UTC
                                                    )
