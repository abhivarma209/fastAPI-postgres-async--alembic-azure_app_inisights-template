"""update table name

Revision ID: 63f9b3edf831
Revises: f4f4c3b6d6b4
Create Date: 2025-10-29 23:46:24.390214

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '63f9b3edf831'
down_revision: Union[str, Sequence[str], None] = 'f4f4c3b6d6b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.rename_table('inventory_status_mappings', 'inventory_status_mapping')


def downgrade() -> None:
    """Downgrade schema."""
    op.rename_table('inventory_status_mapping', 'inventory_status_mappings')
