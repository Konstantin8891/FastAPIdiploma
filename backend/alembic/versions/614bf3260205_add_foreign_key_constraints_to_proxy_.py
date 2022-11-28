"""Add foreign key constraints to proxy tables

Revision ID: 614bf3260205
Revises: 4d06b25ed5cb
Create Date: 2022-11-24 21:10:56.808105

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '614bf3260205'
down_revision = '4d06b25ed5cb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_foreign_key(
        'ingredient_fk',
        source_table='ingredient_recipe_relation',
        referent_table='ingredient',
        local_cols=['ingredient_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )
    op.create_foreign_key(
        'recipe_fk',
        source_table='ingredient_recipe_relation',
        referent_table='recipe',
        local_cols=['recipe_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )
    op.create_foreign_key(
        'tag_fk',
        source_table='tag_recipe_relation',
        referent_table='tag',
        local_cols=['tag_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )
    op.create_foreign_key(
        'recipe_fk',
        source_table='tag_recipe_relation',
        referent_table='recipe',
        local_cols=['recipe_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    op.drop_constraint('ingredient_fk', table_name='ingredient_recipe_relation')
    op.drop_constraint('recipe_fk', table_name='ingredient_recipe_relation')
    op.drop_constraint('tag_fk', table_name='tag_recipe_relation')
    op.drop_constraint('recipe_fk', table_name='tag_recipe_relation')
