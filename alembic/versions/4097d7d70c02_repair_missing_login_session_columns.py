"""repair missing login session columns

Revision ID: 4097d7d70c02
Revises: 15e47e4fbed4
Create Date: 2026-07-29

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "4097d7d70c02"
down_revision: Union[str, Sequence[str], None] = "15e47e4fbed4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "login_sessions",
        sa.Column("user_agent", sa.String(), nullable=True)
    )

    op.add_column(
        "login_sessions",
        sa.Column("refresh_jti", sa.String(), nullable=True)
    )

    op.add_column(
        "login_sessions",
        sa.Column("login_at", sa.DateTime(), nullable=True)
    )

    op.add_column(
        "login_sessions",
        sa.Column("last_seen", sa.DateTime(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("login_sessions", "last_seen")
    op.drop_column("login_sessions", "login_at")
    op.drop_column("login_sessions", "refresh_jti")
    op.drop_column("login_sessions", "user_agent")
