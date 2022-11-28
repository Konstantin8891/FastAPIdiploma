"""Add manytomany proxytables

Revision ID: ec9e0bca1b76
Revises: 65e5044aa27c
Create Date: 2022-11-24 17:57:23.617329

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec9e0bca1b76'
down_revision = '65e5044aa27c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'ingredient_recipe_relation',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('ingredient_id', sa.Integer(), nullable=False),
        sa.Column('recipe_id', sa.Integer(), nullable=False)
    )
    op.create_table(
        'tag_recipe_relation',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('tag_id', sa.Integer(), nullable=False),
        sa.Column('recipe_id', sa.Integer(), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('ingredient_recipe_relation')
    op.drop_table('tag_recipe_relation')
