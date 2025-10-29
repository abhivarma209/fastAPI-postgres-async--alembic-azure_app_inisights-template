"""remove old sap rules

Revision ID: f4f4c3b6d6b4
Revises: 8e950d545ac6
Create Date: 2025-09-30 21:12:56.080538

"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql.base import UUID

# revision identifiers, used by Alembic.
revision: str = 'f4f4c3b6d6b4'
down_revision: Union[str, Sequence[str], None] = '8e950d545ac6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    inventory_status_mappings = sa.table(
        "inventory_status_mappings",
        sa.column("id", UUID(as_uuid=True)),
        sa.column("source_system", sa.String),
        sa.column("column_mappings", sa.JSON),
        sa.column("result_status", sa.String),
        sa.column("description", sa.Text),
        sa.column("priority", sa.Integer),
        sa.column("is_active", sa.Boolean),
    )

    conn = op.get_bind()
    conn.execute(
        sa.text("DELETE FROM inventory_status_mappings WHERE source_system = 'sap'")
    )

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
                "priority": 0,
                "is_active": True,
            },
            {
                "id": str(uuid.uuid4()),
                "source_system": "sap",
                "column_mappings": [
                    {"column_name": "Status", "column_value": "Discarded"}
                ],
                "result_status": "Block",
                "priority": 1,
                "is_active": True,
            },
            {
                "id": str(uuid.uuid4()),
                "source_system": "sap",
                "column_mappings": [
                    {"column_name": "Status", "column_value": "Explanted"}
                ],
                "result_status": "Block",
                "priority": 2,
                "is_active": True,
            },
            {
                "id": str(uuid.uuid4()),
                "source_system": "sap",
                "column_mappings": [{"column_name": "Status", "column_value": "Lost"}],
                "result_status": "Block",
                "priority": 3,
                "is_active": True,
            },
            {
                "id": str(uuid.uuid4()),
                "source_system": "sap",
                "column_mappings": [
                    {"column_name": "Status", "column_value": "Warehouse"}
                ],
                "result_status": "Block",
                "priority": 4,
                "is_active": True,
            },
            {
                "id": str(uuid.uuid4()),
                "source_system": "sap",
                "column_mappings": [
                    {"column_name": "Status", "column_value": "Reported by Doctor"}
                ],
                "result_status": "Unrestricted",
                "priority": 10,
                "is_active": True,
            },
            {
                "id": str(uuid.uuid4()),
                "source_system": "sap",
                "column_mappings": [
                    {"column_name": "Status", "column_value": "Reported by Patient"}
                ],
                "result_status": "Unrestricted",
                "priority": 11,
                "is_active": True,
            },
            {
                "id": str(uuid.uuid4()),
                "source_system": "sap",
                "column_mappings": [
                    {"column_name": "Status", "column_value": "Shipped to the Clinic"}
                ],
                "result_status": "Unrestricted",
                "priority": 12,
                "is_active": True,
            }
        ]
    )


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        sa.text("DELETE FROM inventory_status_mappings WHERE source_system = 'sap'")
    )
