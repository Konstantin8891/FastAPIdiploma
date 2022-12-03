"""create favorite table

Revision ID: 0e863f0d59dd
Revises: 781e12a9de82
Create Date: 2022-12-02 20:47:03.396871

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e863f0d59dd'
down_revision = '781e12a9de82'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'favorite',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('recipe_id', sa.Integer(), nullable=False)
    )
    op.create_foreign_key(
        'favorite_users_fk',
        source_table='favorite',
        referent_table='user',
        local_cols=['user_id'],
        remote_cols=['id']
    )
    op.create_foreign_key(
        'favorite_recipes_fk',
        source_table='favorite',
        referent_table='recipe',
        local_cols=['recipe_id'],
        remote_cols=['id']
    )


def downgrade() -> None:
    op.drop_constraint('favorite_recipes_fk', table_name='favorite')
    op.drop_constraint('favorite_users_fk', table_name='favorite')
    op.drop_table('favorite')
