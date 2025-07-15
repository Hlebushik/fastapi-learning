"""create posts table

Revision ID: b585f5aab5e3
Revises: 
Create Date: 2025-07-15 19:21:56.788795

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b585f5aab5e3'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer, primary_key=True, nullable=False, index=True),
                    sa.Column('title', sa.String, index=True, nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
