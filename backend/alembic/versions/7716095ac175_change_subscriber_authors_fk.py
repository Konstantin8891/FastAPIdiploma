"""Change subscriber_authors_fk

Revision ID: 7716095ac175
Revises: 879b82e3c5bb
Create Date: 2022-12-08 18:59:08.253025

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7716095ac175'
down_revision = '879b82e3c5bb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_constraint('subscriber_authors_fk', table_name='subscriber')
    op.create_foreign_key(
        'subscriber_authors_fk',
        source_table='subscriber',
        referent_table='user',
        local_cols=['author_id'],
        remote_cols=['id']
    )


def downgrade() -> None:
    op.drop_constraint('subscriber_authors_fk', table_name='subscriber')
    op.create_foreign_key(
        'subscriber_authors_fk',
        source_table='subscriber',
        referent_table='recipe',
        local_cols=['author_id'],
        remote_cols=['id']
    )
