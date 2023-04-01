"""Add image_id

Revision ID: ac063335f9b0
Revises: e1eb96fa081e
Create Date: 2023-03-09 15:13:35.614134

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac063335f9b0'
down_revision = 'e1eb96fa081e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('recipe', sa.Column('image_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'recipe_image_fk',
        source_table='recipe',
        referent_table='image',
        local_cols=['image_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    op.drop_constraint('recipe_image_fk', table_name='recipe')
    op.drop_column('recipe', 'image_id')
