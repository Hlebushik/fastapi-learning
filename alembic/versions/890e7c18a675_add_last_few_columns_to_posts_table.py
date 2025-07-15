"""add last few columns to posts table

Revision ID: 890e7c18a675
Revises: 5ce4fed52e23
Create Date: 2025-07-15 20:04:03.368550

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '890e7c18a675'
down_revision: Union[str, Sequence[str], None] = '5ce4fed52e23'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('published', sa.Boolean, server_default='TRUE', nullable=False))
    op.add_column(
        'posts',
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))                  
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
