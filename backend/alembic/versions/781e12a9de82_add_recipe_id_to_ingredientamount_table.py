"""Add recipe_id to ingredientamount table

Revision ID: 781e12a9de82
Revises: 92b5a8a04415
Create Date: 2022-12-02 16:24:35.789784

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '781e12a9de82'
down_revision = '92b5a8a04415'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'ingredient_amount',
        sa.Column('recipe_id', sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        'ingredient_recipe_fk',
        source_table='ingredient_amount',
        referent_table='recipe',
        local_cols=['recipe_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    op.drop_constraint('ingredient_recipe_fk', table_name='ingredient_amount')
    op.drop_column('ingredient_amount', 'recipe_id')
