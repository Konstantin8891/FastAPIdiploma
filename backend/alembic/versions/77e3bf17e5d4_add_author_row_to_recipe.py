"""Add author row to recipe

Revision ID: 77e3bf17e5d4
Revises: 84396d405b4a
Create Date: 2022-11-24 21:57:54.643373

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77e3bf17e5d4'
down_revision = '84396d405b4a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'recipe',
        sa.Column('author_id', sa.Integer(), nullable=False)
    )
    op.create_foreign_key(
        'recipe_users_fk',
        source_table='recipe',
        referent_table='user',
        local_cols=['author_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    op.drop_constraint('recipe_users_fk', table_name='recipe')
    op.drop_column('recipe', 'author_id')
