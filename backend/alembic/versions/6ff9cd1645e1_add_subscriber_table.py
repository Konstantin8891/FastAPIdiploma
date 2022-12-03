"""Add subscriber table

Revision ID: 6ff9cd1645e1
Revises: d5b67383b0a2
Create Date: 2022-12-03 16:33:33.304349

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6ff9cd1645e1'
down_revision = 'd5b67383b0a2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'subscriber',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('author_id', sa.Integer(), nullable=False)
    )
    op.create_foreign_key(
        'subscriber_users_fk',
        source_table='subscriber',
        referent_table='user',
        local_cols=['user_id'],
        remote_cols=['id']
    )
    op.create_foreign_key(
        'subscriber_authors_fk',
        source_table='subscriber',
        referent_table='recipe',
        local_cols=['author_id'],
        remote_cols=['id']
    )


def downgrade() -> None:
    op.drop_constraint('subscriber_authors_fk', table_name='subscriber')
    op.drop_constraint('subscriber_users_fk', table_name='subscriber')
    op.drop_table('subscriber')
