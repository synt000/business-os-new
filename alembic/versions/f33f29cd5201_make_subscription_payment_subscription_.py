"""make subscription payment subscription nullable

Revision ID: f33f29cd5201
Revises: 9cc7a0158927
Create Date: 2026-07-29 18:12:32.016138

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f33f29cd5201'
down_revision: Union[str, Sequence[str], None] = '9cc7a0158927'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "subscription_payments",
        "subscription_id",
        existing_type=sa.String(),
        nullable=True,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "subscription_payments",
        "subscription_id",
        existing_type=sa.String(),
        nullable=False,
    )
