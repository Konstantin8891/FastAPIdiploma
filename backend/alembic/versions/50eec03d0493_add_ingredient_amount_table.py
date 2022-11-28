"""Add ingredient amount table

Revision ID: 50eec03d0493
Revises: 614bf3260205
Create Date: 2022-11-24 21:25:21.530224

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50eec03d0493'
down_revision = '614bf3260205'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'ingredient_amount',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('ingredient_id', sa.Integer(), nullable=False),
        sa.Column('amount', sa.Integer(), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('ingredient_amount')
