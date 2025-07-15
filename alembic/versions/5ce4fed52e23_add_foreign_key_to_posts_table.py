"""add foreign-key to posts table

Revision ID: 5ce4fed52e23
Revises: f602dcd664f8
Create Date: 2025-07-15 19:59:32.258356

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5ce4fed52e23'
down_revision: Union[str, Sequence[str], None] = 'f602dcd664f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('owner_id', sa.Integer, nullable=False)) 
    op.create_foreign_key('post_user_fk', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('post_user_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
