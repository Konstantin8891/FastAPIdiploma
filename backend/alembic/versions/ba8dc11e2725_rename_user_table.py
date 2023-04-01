"""Rename user table

Revision ID: ba8dc11e2725
Revises: 992916166e3c
Create Date: 2023-03-27 19:12:38.392665

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba8dc11e2725'
down_revision = '992916166e3c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.rename_table('user', 'users')


def downgrade() -> None:
    op.rename_table('users', 'user')
