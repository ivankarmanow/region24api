"""created at orphographic error

Revision ID: d8a51fde0350
Revises: a20011251d56
Create Date: 2025-05-21 06:10:00.432965

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd8a51fde0350'
down_revision: Union[str, None] = 'a20011251d56'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    # op.add_column('order', sa.Column('created_at', sa.DateTime(), nullable=False))
    # op.drop_column('order', 'creaeted_at')
    # ### end Alembic commands ###
    op.alter_column('order', 'creaeted_at', new_column_name='created_at', type_=sa.DateTime)


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    # op.add_column('order', sa.Column('creaeted_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    # op.drop_column('order', 'created_at')
    # ### end Alembic commands ###
    op.alter_column('order', 'created_at', new_column_name='creaeted_at', type_=sa.DateTime)
