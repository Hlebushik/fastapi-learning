"""auto-vote

Revision ID: aeba1eab9e35
Revises: 890e7c18a675
Create Date: 2025-07-15 20:11:41.844519

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aeba1eab9e35'
down_revision: Union[str, Sequence[str], None] = '890e7c18a675'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    # op.drop_constraint(op.f('users_email_key'), 'users', type_='unique')
    # op.drop_index(op.f('ix_users_email'), table_name='users')
    # op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_index(op.f('ix_users_email'), table_name='users')
    # op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=False)
    # op.create_unique_constraint(op.f('users_email_key'), 'users', ['email'])
    op.drop_table('votes')
    # ### end Alembic commands ###
