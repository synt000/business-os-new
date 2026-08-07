"""add customer payments table

Revision ID: 209b27b2b614
Revises: 8aa788e5f7e1
Create Date: 2026-08-05

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "209b27b2b614"
down_revision: Union[str, Sequence[str], None] = "8aa788e5f7e1"
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table(
        "customer_payments",

        sa.Column(
            "id",
            sa.String(),
            primary_key=True
        ),

        sa.Column(
            "payment_number",
            sa.String(),
            nullable=False
        ),

        sa.Column(
            "customer_id",
            sa.String(),
            nullable=False
        ),

        sa.Column(
            "receivable_id",
            sa.String(),
            nullable=False
        ),

        sa.Column(
            "amount",
            sa.Float(),
            nullable=False
        ),

        sa.Column(
            "payment_method",
            sa.String(),
            nullable=False
        ),

        sa.Column(
            "status",
            sa.String(),
            nullable=False
        ),

        sa.Column(
            "tenant_id",
            sa.String(),
            nullable=False
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=True
        ),

        sa.ForeignKeyConstraint(
            ["customer_id"],
            ["customers.id"]
        ),

        sa.ForeignKeyConstraint(
            ["receivable_id"],
            ["receivables.id"]
        ),

        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenants.id"]
        ),
    )


def downgrade() -> None:

    op.drop_table("customer_payments")
