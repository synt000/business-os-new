"""phase-7.3C add customer address model

Revision ID: 8aa788e5f7e1
Revises: 1b7f2fe886a7
Create Date: 2026-08-04
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "8aa788e5f7e1"
down_revision: Union[str, Sequence[str], None] = "1b7f2fe886a7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "customer_addresses",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("tenant_id", sa.String(), nullable=False),
        sa.Column("customer_id", sa.String(), nullable=False),
        sa.Column("address_type", sa.String(), nullable=False),
        sa.Column("line1", sa.String(), nullable=False),
        sa.Column("city", sa.String(), nullable=True),
        sa.Column("township", sa.String(), nullable=True),
        sa.Column("phone", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),

        sa.ForeignKeyConstraint(
            ["customer_id"],
            ["customers.id"],
            ondelete="CASCADE",
        ),

        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenants.id"],
            ondelete="CASCADE",
        ),

        sa.PrimaryKeyConstraint("id"),
    )


    op.create_index(
        "ix_customer_addresses_customer_id",
        "customer_addresses",
        ["customer_id"],
    )

    op.create_index(
        "ix_customer_addresses_tenant_id",
        "customer_addresses",
        ["tenant_id"],
    )

    op.create_index(
        "ix_customer_addresses_id",
        "customer_addresses",
        ["id"],
    )


def downgrade() -> None:

    op.drop_index(
        "ix_customer_addresses_id",
        table_name="customer_addresses",
    )

    op.drop_index(
        "ix_customer_addresses_tenant_id",
        table_name="customer_addresses",
    )

    op.drop_index(
        "ix_customer_addresses_customer_id",
        table_name="customer_addresses",
    )

    op.drop_table("customer_addresses")
