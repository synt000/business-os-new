"""add security event risk enrichment fields

Revision ID: 101ae713a972
Revises: 912de7891b6a
Create Date: 2026-07-30 00:40:48.903829

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '101ae713a972'
down_revision: Union[str, Sequence[str], None] = '912de7891b6a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "security_events",
        sa.Column(
            "login_session_id",
            sa.String(),
            nullable=True
        )
    )

    op.add_column(
        "security_events",
        sa.Column(
            "device_session_id",
            sa.String(),
            nullable=True
        )
    )

    op.add_column(
        "security_events",
        sa.Column(
            "risk_score",
            sa.String(),
            nullable=True
        )
    )

    op.add_column(
        "security_events",
        sa.Column(
            "risk_level",
            sa.String(),
            nullable=True
        )
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("security_events", "risk_level")
    op.drop_column("security_events", "risk_score")
    op.drop_column("security_events", "device_session_id")
    op.drop_column("security_events", "login_session_id")
