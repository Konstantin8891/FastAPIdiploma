"""Change foreignkey in ingredient_recipe_relation

Revision ID: 879b82e3c5bb
Revises: 6ff9cd1645e1
Create Date: 2022-12-05 15:27:19.249566

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '879b82e3c5bb'
down_revision = '6ff9cd1645e1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_constraint(
        'ingredient_fk', table_name='ingredient_recipe_relation'
    )
    op.create_foreign_key(
        'ingredient_fk',
        source_table='ingredient_recipe_relation',
        referent_table='ingredient_amount',
        local_cols=['ingredient_id'],
        remote_cols=['id'],
        ondelete='CASCADE'

    )

def downgrade() -> None:
    op.drop_constraint('ingredient_fk', 'ingredient_recipe_relation')
    op.create_foreign_key(
        'ingredient_fk',
        source_table='ingredient_recipe_relation',
        referent_table='ingredient',
        local_cols=['ingredient_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )
