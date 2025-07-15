"""add user table

Revision ID: f602dcd664f8
Revises: ed44fa700e06
Create Date: 2025-07-15 19:53:24.534510

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f602dcd664f8'
down_revision: Union[str, Sequence[str], None] = 'ed44fa700e06'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, nullable=False, index=True),
        sa.Column('email', sa.String, index=True, nullable=False),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )   
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
