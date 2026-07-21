"""add hospitals (multi-tenant) and super_admin role

Revision ID: 0002
Revises: 0001
Create Date: 2026-07-21

"""
import uuid
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0002"
down_revision: str | None = "0001"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "hospitals",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("code", sa.String(length=30), nullable=False, unique=True),
        sa.Column("address", sa.String(length=255), nullable=True),
        sa.Column("phone", sa.String(length=20), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_hospitals_code", "hospitals", ["code"])

    op.add_column(
        "staff",
        sa.Column("hospital_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("hospitals.id"), nullable=True),
    )

    roles_table = sa.table(
        "roles",
        sa.column("id", postgresql.UUID(as_uuid=True)),
        sa.column("name", sa.String),
    )
    op.bulk_insert(roles_table, [{"id": uuid.uuid4(), "name": "super_admin"}])


def downgrade() -> None:
    op.drop_column("staff", "hospital_id")
    op.drop_index("ix_hospitals_code", table_name="hospitals")
    op.drop_table("hospitals")

    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM roles WHERE name = 'super_admin'"))
