"""add content column to posts table

Revision ID: ed44fa700e06
Revises: b585f5aab5e3
Create Date: 2025-07-15 19:48:35.171027

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ed44fa700e06'
down_revision: Union[str, Sequence[str], None] = 'b585f5aab5e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
