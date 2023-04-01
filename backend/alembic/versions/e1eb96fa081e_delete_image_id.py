"""Delete image_id

Revision ID: e1eb96fa081e
Revises: ae3fa53b986b
Create Date: 2023-03-09 15:12:21.811277

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1eb96fa081e'
down_revision = 'ae3fa53b986b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column('recipe', 'image_id')


def downgrade() -> None:
    op.add_column('recipe', sa.Column('image_id', sa.Integer(), nullable=True))
