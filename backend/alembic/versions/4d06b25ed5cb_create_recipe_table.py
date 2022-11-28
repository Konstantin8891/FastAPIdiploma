"""Create recipe table

Revision ID: 4d06b25ed5cb
Revises: ec9e0bca1b76
Create Date: 2022-11-24 18:45:27.632398

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d06b25ed5cb'
down_revision = 'ec9e0bca1b76'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'recipe',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('image', sa.LargeBinary(), nullable=False),
        sa.Column('text', sa.String(), nullable=False),
        sa.Column('cooking_time', sa.Integer(), nullable=False),
        sa.Column('created', sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('recipe')
