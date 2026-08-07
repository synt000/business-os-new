"""add payment method configuration tables

Revision ID: 73894027a25f
Revises: ed168d6e19e1
Create Date: 2026-08-06 01:16:26.612545

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "73894027a25f"
down_revision: Union[str, Sequence[str], None] = "ed168d6e19e1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "payment_methods",
        sa.Column("code", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("category", sa.String(), nullable=False),
        sa.Column("ledger_account", sa.String(), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=True),
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )

    op.create_table(
        "tenant_payment_methods",
        sa.Column("tenant_id", sa.String(), nullable=False),
        sa.Column("payment_method_id", sa.String(), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=True),
        sa.Column("is_default", sa.Boolean(), nullable=True),
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["payment_method_id"],
            ["payment_methods.id"],
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenants.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table("tenant_payment_methods")
    op.drop_table("payment_methods")
