"""Add column name to recipes table

Revision ID: 84396d405b4a
Revises: 3b183da59ec3
Create Date: 2022-11-24 21:48:40.409312

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84396d405b4a'
down_revision = '3b183da59ec3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint(
        'uq_recipe_name',
        'recipe',
        ['name']
    )


def downgrade() -> None:
    op.drop_constraint('uq_recipe_name', 'name')
