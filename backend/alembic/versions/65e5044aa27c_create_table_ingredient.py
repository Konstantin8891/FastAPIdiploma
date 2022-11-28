"""Create table ingredient

Revision ID: 65e5044aa27c
Revises: db90c77d4adc
Create Date: 2022-11-24 13:58:31.811896

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65e5044aa27c'
down_revision = 'db90c77d4adc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'ingredient',
        sa.Column('id', sa.Integer(), nullable=True, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('measurement_unit', sa.String(), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('ingredient')
