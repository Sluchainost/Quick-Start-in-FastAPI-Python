# pylint: disable-all
# flake8: noqa

"""initial

Revision ID: 9ec4c28d2360
Revises: f87248302e65
Create Date: 2025-03-17 14:38:59.513278

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ec4c28d2360'
down_revision: Union[str, None] = 'f87248302e65'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
