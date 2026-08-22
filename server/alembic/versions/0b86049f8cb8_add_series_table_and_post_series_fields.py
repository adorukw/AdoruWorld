"""add series table and post series fields

Revision ID: 0b86049f8cb8
Revises: b94c5a3a62fe
Create Date: 2026-08-22 16:51:05.495341

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0b86049f8cb8'
down_revision: Union[str, Sequence[str], None] = 'b94c5a3a62fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


FK_NAME = "fk_posts_series_id_series"


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('series',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('slug', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('cover_image', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('slug')
    )
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('series_id', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('series_order', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(FK_NAME, 'series', ['series_id'], ['id'], ondelete='SET NULL')

    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_constraint(FK_NAME, type_='foreignkey')
        batch_op.drop_column('series_order')
        batch_op.drop_column('series_id')

    op.drop_table('series')
    # ### end Alembic commands ###
