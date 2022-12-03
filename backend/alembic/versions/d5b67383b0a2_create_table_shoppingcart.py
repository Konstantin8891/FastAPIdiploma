"""Create table shoppingcart

Revision ID: d5b67383b0a2
Revises: 0e863f0d59dd
Create Date: 2022-12-03 14:54:09.741660

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5b67383b0a2'
down_revision = '0e863f0d59dd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'shopping_cart',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('recipe_id', sa.Integer(), nullable=False)
    )
    op.create_foreign_key(
        'shoppingcart_users_fk',
        source_table='shopping_cart',
        referent_table='user',
        local_cols=['user_id'],
        remote_cols=['id']
    )
    op.create_foreign_key(
        'shoppingcart_recipes_fk',
        source_table='shopping_cart',
        referent_table='recipe',
        local_cols=['recipe_id'],
        remote_cols=['id']
    )


def downgrade() -> None:
    op.drop_constraint('shoppingcart_recipes_fk', table_name='shopping_cart')
    op.drop_constraint('shoppingcart_users_fk', table_name='shopping_cart')
    op.drop_table('shopping_cart')
