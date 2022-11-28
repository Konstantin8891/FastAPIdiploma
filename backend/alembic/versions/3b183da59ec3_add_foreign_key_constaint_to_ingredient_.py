"""Add foreign key constaint to ingredient amount table

Revision ID: 3b183da59ec3
Revises: 50eec03d0493
Create Date: 2022-11-24 21:29:41.288503

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b183da59ec3'
down_revision = '50eec03d0493'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_foreign_key(
        'ingredient_fk',
        source_table='ingredient_amount',
        referent_table='ingredient',
        local_cols=['ingredient_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    op.drop_constraint('ingredient_fk', table_name='ingredient_amount')
