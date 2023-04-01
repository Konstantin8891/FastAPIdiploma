"""Change field url type

Revision ID: 04c40eded7eb
Revises: 1d08eed28845
Create Date: 2023-03-27 18:45:19.623975

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy_utils import URLType


# revision identifiers, used by Alembic.
revision = '04c40eded7eb'
down_revision = '1d08eed28845'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('image', 'url',
                    existing_type=sa.String(),
                    type_=URLType())


def downgrade() -> None:
    op.alter_column('user', 'email',
                    existing_type=URLType(),
                    type_=sa.String())