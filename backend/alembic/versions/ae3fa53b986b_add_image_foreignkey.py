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