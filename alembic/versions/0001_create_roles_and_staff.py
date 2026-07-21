"""create roles and staff tables

Revision ID: 0001
Revises:
Create Date: 2026-07-20

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "0001"
down_revision: str | None = None
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None

ROLE_NAMES = [
    "admin",
    "receptionist",
    "billing_clerk",
    "triage_nurse",
    "doctor",
    "lab_tech",
    "pharmacist",
    "admission_officer",
    "ward_nurse",
    "consultant",
    "records_officer",
]


def upgrade() -> None:
    op.create_table(
        "roles",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(length=50), nullable=False, unique=True),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_roles_name", "roles", ["name"])

    op.create_table(
        "staff",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("full_name", sa.String(length=150), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("phone", sa.String(length=20), nullable=True),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("role_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("roles.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_staff_email", "staff", ["email"])

    # Seed the fixed role set
    roles_table = sa.table(
        "roles",
        sa.column("id", postgresql.UUID(as_uuid=True)),
        sa.column("name", sa.String),
    )
    import uuid

    op.bulk_insert(roles_table, [{"id": uuid.uuid4(), "name": name} for name in ROLE_NAMES])


def downgrade() -> None:
    op.drop_index("ix_staff_email", table_name="staff")
    op.drop_table("staff")
    op.drop_index("ix_roles_name", table_name="roles")
    op.drop_table("roles")
