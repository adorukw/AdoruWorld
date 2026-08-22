"""restrict category deletion on posts

Revision ID: b94c5a3a62fe
Revises: addd6d295de9
Create Date: 2026-08-22 16:37:32.898134

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b94c5a3a62fe'
down_revision: Union[str, Sequence[str], None] = 'addd6d295de9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


FK_NAME = "fk_posts_category_id_post_categories"

# SQLite 反射出的外键没有名字，batch 的 drop_constraint 按名字定位约束，
# 因此传入 naming_convention 让反射约束获得确定名字
NAMING_CONVENTION = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table(
        "posts", naming_convention=NAMING_CONVENTION
    ) as batch_op:
        batch_op.drop_constraint(FK_NAME, type_="foreignkey")
        batch_op.create_foreign_key(
            FK_NAME, "post_categories", ["category_id"], ["id"], ondelete="RESTRICT"
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table(
        "posts", naming_convention=NAMING_CONVENTION
    ) as batch_op:
        batch_op.drop_constraint(FK_NAME, type_="foreignkey")
        batch_op.create_foreign_key(
            FK_NAME, "post_categories", ["category_id"], ["id"], ondelete="SET NULL"
        )
