"""add bank reconciliation foundation

Revision ID: 3efc24b95335
Revises: 73894027a25f
Create Date: 2026-08-07 21:48:42.111871

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "3efc24b95335"
down_revision: Union[str, Sequence[str], None] = "73894027a25f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "bank_transactions",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("tenant_id", sa.String(), nullable=False),
        sa.Column("bank_name", sa.String(), nullable=False),
        sa.Column("account_number", sa.String(), nullable=True),
        sa.Column("transaction_date", sa.DateTime(), nullable=False),
        sa.Column("external_reference", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("direction", sa.String(), nullable=False),
        sa.Column("matched_payment_id", sa.String(), nullable=True),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenants.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "idx_bank_tx_tenant_status",
        "bank_transactions",
        ["tenant_id", "status"],
    )

    op.create_index(
        "ix_bank_transactions_created_at",
        "bank_transactions",
        ["created_at"],
    )

    op.create_index(
        "ix_bank_transactions_external_reference",
        "bank_transactions",
        ["external_reference"],
    )

    op.create_index(
        "ix_bank_transactions_matched_payment_id",
        "bank_transactions",
        ["matched_payment_id"],
    )

    op.create_index(
        "ix_bank_transactions_status",
        "bank_transactions",
        ["status"],
    )

    op.create_index(
        "ix_bank_transactions_tenant_id",
        "bank_transactions",
        ["tenant_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_bank_transactions_tenant_id",
        table_name="bank_transactions",
    )

    op.drop_index(
        "ix_bank_transactions_status",
        table_name="bank_transactions",
    )

    op.drop_index(
        "ix_bank_transactions_matched_payment_id",
        table_name="bank_transactions",
    )

    op.drop_index(
        "ix_bank_transactions_external_reference",
        table_name="bank_transactions",
    )

    op.drop_index(
        "ix_bank_transactions_created_at",
        table_name="bank_transactions",
    )

    op.drop_index(
        "idx_bank_tx_tenant_status",
        table_name="bank_transactions",
    )

    op.drop_table("bank_transactions")
