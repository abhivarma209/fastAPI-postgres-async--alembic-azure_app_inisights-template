"""add old inventory statuses

Revision ID: 8e950d545ac6
Revises: 5b1cb92ead8a
Create Date: 2025-09-29 09:54:16.730779

"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql.base import UUID

# revision identifiers, used by Alembic.
revision: str = '8e950d545ac6'
down_revision: Union[str, Sequence[str], None] = '5b1cb92ead8a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    inventory_status_mappings = sa.table(
        'inventory_status_mappings',
        sa.column('id', UUID(as_uuid=True)),
        sa.column('source_system', sa.String),
        sa.column('column_mappings', sa.JSON),
        sa.column('result_status', sa.String),
        sa.column('description', sa.Text),
        sa.column('priority', sa.Integer),
        sa.column('is_active', sa.Boolean),
    )

    # Insert new data
    op.bulk_insert(
        inventory_status_mappings,
        [
            # SAP
            {
                "id": str(uuid.uuid4()),
                "source_system": "sap",
                "column_mappings": [{"column_name": "Stock Type", "column_value": None}],
                "result_status": "Not Found",
                "priority": 0,
                "is_active": True,
            },
            {
                "id": str(uuid.uuid4()),
                "source_system": "sap",
                "column_mappings": [{"column_name": "Stock Type", "column_value": "01"}],
                "result_status": "Unrestricted",
                "priority": 1,
                "is_active": True,
            },
            {
                "id": str(uuid.uuid4()),
                "source_system": "sap",
                "column_mappings": [{"column_name": "Stock Type", "column_value": "1"}],
                "result_status": "Unrestricted",
                "priority": 2,
                "is_active": True,
            },
            {
                "id": str(uuid.uuid4()),
                "source_system": "sap",
                "column_mappings": [{"column_name": "Stock Type", "column_value": "07"}],
                "result_status": "Block",
                "priority": 3,
                "is_active": True,
            },
            {
                "id": str(uuid.uuid4()),
                "source_system": "sap",
                "column_mappings": [{"column_name": "Stock Type", "column_value": "7"}],
                "result_status": "Block",
                "priority": 4,
                "is_active": True,
            },
            # Logiwa
            {
                "id": str(uuid.uuid4()),
                "source_system": "logiwa",
                "column_mappings": [{"column_name": "Inventory Status", "column_value": None}],
                "result_status": "Not Found",
                "priority": 0,
                "is_active": True,
            },
            {
                "id": str(uuid.uuid4()),
                "source_system": "logiwa",
                "column_mappings": [{"column_name": "Suitability Reason", "column_value": "*"}],
                "result_status": "Block",
                "priority": 1,
                "is_active": True,
            },
            {
                "id": str(uuid.uuid4()),
                "source_system": "logiwa",
                "column_mappings": [{"column_name": "Quarantine Reason", "column_value": "*"}],
                "result_status": "Block",
                "priority": 2,
                "is_active": True,
            },
            # Spyglass
            {
                "id": str(uuid.uuid4()),
                "source_system": "spyglass",
                "column_mappings": [{"column_name": "Status", "column_value": None}],
                "result_status": "Not Found",
                "priority": 0,
                "is_active": True,
            },
            {
                "id": str(uuid.uuid4()),
                "source_system": "spyglass",
                "column_mappings": [{"column_name": "Status", "column_value": "Available"}],
                "result_status": "Unrestricted",
                "priority": 1,
                "is_active": True,
            },
            {
                "id": str(uuid.uuid4()),
                "source_system": "spyglass",
                "column_mappings": [{"column_name": "Status", "column_value": "Blocked"}],
                "result_status": "Block",
                "priority": 2,
                "is_active": True,
            },
            {
                "id": str(uuid.uuid4()),
                "source_system": "spyglass",
                "column_mappings": [{"column_name": "Status", "column_value": "Committed"}],
                "result_status": "Committed",
                "priority": 3,
                "is_active": True,
            },
        ]
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
