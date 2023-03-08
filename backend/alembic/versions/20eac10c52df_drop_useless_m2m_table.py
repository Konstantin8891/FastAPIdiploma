"""drop useless m2m table

Revision ID: 20eac10c52df
Revises: 7716095ac175
Create Date: 2023-01-26 14:07:41.804923

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20eac10c52df'
down_revision = '7716095ac175'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_table('ingredient_recipe_relation')


def downgrade() -> None:
    op.create_table(
        'ingredient_recipe_relation',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('ingredient_id', sa.Integer(), nullable=False),
        sa.Column('recipe_id', sa.Integer(), nullable=False)
    )
