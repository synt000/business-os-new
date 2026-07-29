"""add login risk enrichment fields

Revision ID: 912de7891b6a
Revises: 4097d7d70c02
Create Date: 2026-07-30
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "912de7891b6a"
down_revision: Union[str, Sequence[str], None] = "4097d7d70c02"
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.add_column(
        "login_sessions",
        sa.Column(
            "risk_score",
            sa.String(),
            nullable=True
        )
    )

    op.add_column(
        "login_sessions",
        sa.Column(
            "risk_level",
            sa.String(),
            nullable=True,
            server_default="LOW"
        )
    )

    op.add_column(
        "login_sessions",
        sa.Column(
            "login_type",
            sa.String(),
            nullable=True,
            server_default="PASSWORD"
        )
    )

    op.add_column(
        "login_sessions",
        sa.Column(
            "is_new_device",
            sa.Boolean(),
            nullable=True,
            server_default=sa.text("false")
        )
    )


def downgrade() -> None:

    op.drop_column(
        "login_sessions",
        "is_new_device"
    )

    op.drop_column(
        "login_sessions",
        "login_type"
    )

    op.drop_column(
        "login_sessions",
        "risk_level"
    )

    op.drop_column(
        "login_sessions",
        "risk_score"
    )
