"""sync subscription license schema

Revision ID: fd146b8e6049
Revises: 35e02c1af719
Create Date: 2026-07-27
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = "fd146b8e6049"
down_revision: Union[str, Sequence[str], None] = "35e02c1af719"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Sync subscription/license engine.

    Keep existing business data untouched.
    """

    # activation_keys legacy -> new license engine

    op.alter_column(
        "activation_keys",
        "plan_id",
        existing_type=sa.VARCHAR(),
        nullable=False,
    )


def downgrade() -> None:
    """
    Rollback subscription/license sync.
    """

    op.alter_column(
        "activation_keys",
        "plan_id",
        existing_type=sa.VARCHAR(),
        nullable=True,
    )
