"""verification codes

Revision ID: 2625f383a41d
Revises: 2d140e0e5982
Create Date: 2025-03-28 19:42:30.092752

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2625f383a41d'
down_revision: Union[str, None] = '2d140e0e5982'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('verification_codes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('code', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_verification_codes_code'), 'verification_codes', ['code'], unique=False)
    op.create_index(op.f('ix_verification_codes_email'), 'verification_codes', ['email'], unique=False)
    op.create_index(op.f('ix_verification_codes_id'), 'verification_codes', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_verification_codes_id'), table_name='verification_codes')
    op.drop_index(op.f('ix_verification_codes_email'), table_name='verification_codes')
    op.drop_index(op.f('ix_verification_codes_code'), table_name='verification_codes')
    op.drop_table('verification_codes')
    # ### end Alembic commands ###
