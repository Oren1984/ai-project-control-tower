"""wave4: add reports table

Revision ID: 0003
Revises: 0002
Create Date: 2026-05-02
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0003"
down_revision: Union[str, None] = "0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "reports",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("audit_run_id", sa.Integer(), nullable=False),
        sa.Column("report_format", sa.String(length=20), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("file_path", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.ForeignKeyConstraint(["audit_run_id"], ["audit_runs.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_reports_audit_run_id", "reports", ["audit_run_id"])
    op.create_index("ix_reports_format", "reports", ["report_format"])


def downgrade() -> None:
    op.drop_index("ix_reports_format", "reports")
    op.drop_index("ix_reports_audit_run_id", "reports")
    op.drop_table("reports")
