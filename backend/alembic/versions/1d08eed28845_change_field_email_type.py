"""Change field email type

Revision ID: 1d08eed28845
Revises: ac063335f9b0
Create Date: 2023-03-27 18:38:07.876692

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy_utils import EmailType


# revision identifiers, used by Alembic.
revision = '1d08eed28845'
down_revision = 'ac063335f9b0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('user', 'email',
                    existing_type=sa.String(),
                    type_=EmailType())


def downgrade() -> None:
    op.alter_column('user', 'email',
                    existing_type=EmailType(),
                    type_=sa.String())
