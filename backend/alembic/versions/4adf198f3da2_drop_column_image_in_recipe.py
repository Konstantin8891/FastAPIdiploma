"""Drop column image in recipe

Revision ID: 4adf198f3da2
Revises: 77e3bf17e5d4
Create Date: 2022-11-26 15:51:24.762678

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4adf198f3da2'
down_revision = '77e3bf17e5d4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column('recipe', 'image')


def downgrade() -> None:
    op.add_column(
        'recipe',
        sa.Column(
            'image',
            sa.LargeBinary(),
            nullable=False
        )
    )
