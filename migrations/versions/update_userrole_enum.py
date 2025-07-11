"""Update userrole enum values to uppercase

Revision ID: update_userrole_enum
Revises: add_role_column
Create Date: 2025-07-11 09:02:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'update_userrole_enum'
down_revision: Union[str, None] = 'add_role_column'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Temporarily disable the constraint
    op.execute("ALTER TABLE users ALTER COLUMN role DROP DEFAULT")
    op.execute("ALTER TABLE users ALTER COLUMN role TYPE VARCHAR")
    
    # Drop the old enum type
    op.execute("DROP TYPE userrole")
    
    # Create the new enum type with uppercase values
    op.execute("CREATE TYPE userrole AS ENUM('ADMIN', 'MANAGER', 'USER')")
    
    # Update the existing records to use uppercase values
    op.execute("UPDATE users SET role = upper(role)")
    
    # Convert column back to the enum type and set default
    op.execute("ALTER TABLE users ALTER COLUMN role TYPE userrole USING role::userrole")
    op.execute("ALTER TABLE users ALTER COLUMN role SET DEFAULT 'USER'")


def downgrade() -> None:
    # Temporarily disable the constraint
    op.execute("ALTER TABLE users ALTER COLUMN role DROP DEFAULT")
    op.execute("ALTER TABLE users ALTER COLUMN role TYPE VARCHAR")
    
    # Drop the new enum type
    op.execute("DROP TYPE userrole")
    
    # Create the old enum type with lowercase values
    op.execute("CREATE TYPE userrole AS ENUM('admin', 'manager', 'user')")
    
    # Update the existing records to use lowercase values
    op.execute("UPDATE users SET role = lower(role)")
    
    # Convert column back to the enum type and set default
    op.execute("ALTER TABLE users ALTER COLUMN role TYPE userrole USING role::userrole")
    op.execute("ALTER TABLE users ALTER COLUMN role SET DEFAULT 'user'")
