"""Create table tag

Revision ID: db90c77d4adc
Revises: 7d6a297bd31e
Create Date: 2022-11-24 13:31:11.441267

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db90c77d4adc'
down_revision = '7d6a297bd31e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'tag',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('color', sa.String(), nullable=False),
        sa.Column('slug', sa.String(), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('tag')

