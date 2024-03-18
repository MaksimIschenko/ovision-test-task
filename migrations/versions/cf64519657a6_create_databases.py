"""Create databases

Revision ID: cf64519657a6
Revises: 23942a50d8e9
Create Date: 2024-03-17 16:39:48.746709

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision: str = 'cf64519657a6'
down_revision: Union[str, None] = '23942a50d8e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # check if table already exists and if not, create it
    engine = op.get_bind()
    inspector = inspect(engine)
    if 'images' not in inspector.get_table_names():
        # ### commands auto generated by Alembic - please adjust! ###
        op.create_table('images',
                        sa.Column('id', sa.Integer(), nullable=False),
                        sa.Column('original_image', sa.String(), nullable=False),
                        sa.Column('negative_image', sa.String(), nullable=False),
                        sa.PrimaryKeyConstraint('id')
                        )
        # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('images')
    # ### end Alembic commands ###
