"""add new inventory statuses

Revision ID: 5b1cb92ead8a
Revises: 0487e2a83986
Create Date: 2025-09-26 20:07:40.843607

"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql.base import UUID

# revision identifiers, used by Alembic.
revision: str = '5b1cb92ead8a'
down_revision: Union[str, Sequence[str], None] = '0487e2a83986'
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

    # Delete existing data
    op.execute("DELETE FROM inventory_status_mappings")

    # Insert new data
    op.bulk_insert(
        inventory_status_mappings,
        [
            # SAP New Rules
            {
                "id": str(uuid.uuid4()),
                "source_system": "sap",
                "column_mappings": [{"column_name": "Status", "column_value": None}],
                "result_status": "Not Found",
                "priority": 10,
                "is_active": True,
            },
            {
                "id": str(uuid.uuid4()),
                "source_system": "sap",
                "column_mappings": [{"column_name": "Status", "column_value": "Discarded"}],
                "result_status": "Block",
                "priority": 11,
                "is_active": True,
            },
            {
                "id": str(uuid.uuid4()),
                "source_system": "sap",
                "column_mappings": [{"column_name": "Status", "column_value": "Explanted"}],
                "result_status": "Block",
                "priority": 12,
                "is_active": True,
            },
            {
                "id": str(uuid.uuid4()),
                "source_system": "sap",
                "column_mappings": [{"column_name": "Status", "column_value": "Lost"}],
                "result_status": "Block",
                "priority": 13,
                "is_active": True,
            },
            {
                "id": str(uuid.uuid4()),
                "source_system": "sap",
                "column_mappings": [{"column_name": "Status", "column_value": "Reported by Doctor"}],
                "result_status": "Unrestricted",
                "priority": 14,
                "is_active": True,
            },
            {
                "id": str(uuid.uuid4()),
                "source_system": "sap",
                "column_mappings": [{"column_name": "Status", "column_value": "Reported by Patient"}],
                "result_status": "Unrestricted",
                "priority": 15,
                "is_active": True,
            },
            {
                "id": str(uuid.uuid4()),
                "source_system": "sap",
                "column_mappings": [{"column_name": "Status", "column_value": "Shipped to the Clinic"}],
                "result_status": "Unrestricted",
                "priority": 16,
                "is_active": True,
            },
            {
                "id": str(uuid.uuid4()),
                "source_system": "sap",
                "column_mappings": [{"column_name": "Status", "column_value": "Warehouse"}],
                "result_status": "Block",
                "priority": 17,
                "is_active": True,
            },
            #Salesforce
            {
                "id": str(uuid.uuid4()),
                "source_system": "salesforce",
                "column_mappings": [{"column_name": "Status", "column_value": None}],
                "result_status": "Not Found",
                "priority": 0,
                "is_active": True,
            },
            {
                "id": str(uuid.uuid4()),
                "source_system": "salesforce",
                "column_mappings": [{"column_name": "Status", "column_value": "Damaged"}],
                "result_status": "Block",
                "priority": 5,
                "is_active": True,
            },
            {
                "id": str(uuid.uuid4()),
                "source_system": "salesforce",
                "column_mappings": [{"column_name": "Status", "column_value": "Returned"}],
                "result_status": "Block",
                "priority": 6,
                "is_active": True,
            },
            {
                "id": str(uuid.uuid4()),
                "source_system": "salesforce",
                "column_mappings": [{"column_name": "Status", "column_value": "Available"}],
                "result_status": "Unrestricted",
                "priority": 10,
                "is_active": True,
            },
            {
                "id": str(uuid.uuid4()),
                "source_system": "salesforce",
                "column_mappings": [{"column_name": "Status", "column_value": "In Transfer"}],
                "result_status": "Unrestricted",
                "priority": 11,
                "is_active": True,
            },
            {
                "id": str(uuid.uuid4()),
                "source_system": "salesforce",
                "column_mappings": [{"column_name": "Status", "column_value": "Transferred"}],
                "result_status": "Unrestricted",
                "priority": 12,
                "is_active": True,
            },
            {
                "id": str(uuid.uuid4()),
                "source_system": "salesforce",
                "column_mappings": [{"column_name": "Status", "column_value": "Committed"}],
                "result_status": "Committed",
                "priority": 12,
                "is_active": True,
            },
        ]
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
