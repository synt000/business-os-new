"""add device session binding to login sessions

Revision ID: 15e47e4fbed4
Revises: 1772ed7d397e
Create Date: 2026-07-29
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "15e47e4fbed4"
down_revision: Union[str, Sequence[str], None] = "1772ed7d397e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "login_sessions",
        sa.Column(
            "device_session_id",
            sa.String(),
            nullable=True
        )
    )

    op.create_index(
        "ix_login_sessions_device_session_id",
        "login_sessions",
        ["device_session_id"],
        unique=False
    )

    op.create_foreign_key(
        "fk_login_sessions_device_session_id",
        "login_sessions",
        "device_sessions",
        ["device_session_id"],
        ["id"],
        ondelete="SET NULL"
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_login_sessions_device_session_id",
        "login_sessions",
        type_="foreignkey"
    )

    op.drop_index(
        "ix_login_sessions_device_session_id",
        table_name="login_sessions"
    )

    op.drop_column(
        "login_sessions",
        "device_session_id"
    )
