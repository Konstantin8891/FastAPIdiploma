"""Add role field to user table

Revision ID: 992916166e3c
Revises: 04c40eded7eb
Create Date: 2023-03-27 18:50:14.028312

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy_utils import ChoiceType

import sys
sys.path.append('..')

from models import ROLES

# revision identifiers, used by Alembic.
revision = '992916166e3c'
down_revision = '04c40eded7eb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'user', 
        sa.Column('role', ChoiceType(ROLES), nullable=True)
    )


def downgrade() -> None:
    op.drop_column('user', 'role')
