"""Add image foreignkey

Revision ID: ae3fa53b986b
Revises: 895d954ea268
Create Date: 2023-02-28 14:15:06.312927

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae3fa53b986b'
down_revision = '895d954ea268'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('recipe', sa.Column('image_id', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('recipe', 'image_id')
