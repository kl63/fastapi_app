"""Add role column to users table

Revision ID: add_role_column
Revises: e3a142515f63
Create Date: 2025-07-11 08:58:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_role_column'
down_revision: Union[str, None] = 'e3a142515f63'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create enum type first
    op.execute("CREATE TYPE userrole AS ENUM('admin', 'manager', 'user')")
    
    # Add role column with default value 'user'
    op.add_column('users', sa.Column('role', sa.Enum('admin', 'manager', 'user', name='userrole'), 
                                     nullable=False, server_default='user'))


def downgrade() -> None:
    # Drop role column
    op.drop_column('users', 'role')
    
    # Drop enum type
    op.execute("DROP TYPE userrole")
