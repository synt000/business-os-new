"""add customer payment created at

Revision ID: ed168d6e19e1
Revises: 209b27b2b614
Create Date: 2026-08-05 19:58:10.557057

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ed168d6e19e1'
down_revision: Union[str, Sequence[str], None] = '209b27b2b614'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.execute(
        "UPDATE customer_payments SET created_at = NOW() WHERE created_at IS NULL"
    )

    op.alter_column(
        "customer_payments",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.alter_column(
        "customer_payments",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        nullable=True,
    )
