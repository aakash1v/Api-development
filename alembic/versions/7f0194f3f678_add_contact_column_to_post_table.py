"""add contact column to post table..

Revision ID: 7f0194f3f678
Revises: 351c1a63bf38
Create Date: 2025-01-26 11:43:11.284237

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7f0194f3f678'
down_revision: Union[str, None] = '351c1a63bf38'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
