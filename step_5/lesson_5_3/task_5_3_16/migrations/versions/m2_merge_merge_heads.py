"""Merge heads

Revision ID: m2_merge
Revises: a2_featured, b2_description
Create Date: 2025-06-03 10:56:42.594453

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'm2_merge'
down_revision: Union[str, None] = ('a2_featured', 'b2_description')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
