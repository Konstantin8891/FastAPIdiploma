"""Add image field

Revision ID: 92b5a8a04415
Revises: 4adf198f3da2
Create Date: 2022-11-27 13:32:24.089852

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92b5a8a04415'
down_revision = '4adf198f3da2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'recipe',
        sa.Column('image', sa.String(), nullable=False)
    )


def downgrade() -> None:
    op.drop_column('recipe', 'image')
