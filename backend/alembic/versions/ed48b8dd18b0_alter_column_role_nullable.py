"""Alter column role nullable

Revision ID: ed48b8dd18b0
Revises: ba8dc11e2725
Create Date: 2023-03-27 19:17:40.657617

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed48b8dd18b0'
down_revision = 'ba8dc11e2725'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('users', 'role', nullable=False)


def downgrade() -> None:
    op.alter_column('users', 'role', nullable=True)
