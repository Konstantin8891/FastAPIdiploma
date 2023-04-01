"""Delete field image create table Image

Revision ID: 895d954ea268
Revises: 20eac10c52df
Create Date: 2023-02-28 13:58:32.628398

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '895d954ea268'
down_revision = '20eac10c52df'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column('recipe', 'image')
    op.create_table(
        'image',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('name', sa.Unicode(64), nullable=False),
        sa.Column('path', sa.Unicode(128), nullable=False),
        sa.Column('url', sa.String(), nullable=False)
    )


def downgrade() -> None:
    op.add_column('recipe', sa.Column('image', sa.String(), nullable=True))
    op.drop_table('image')
