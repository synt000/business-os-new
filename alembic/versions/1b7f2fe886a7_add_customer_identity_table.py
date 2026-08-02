"""add_customer_identity_table

Revision ID: 1b7f2fe886a7
Revises: 101ae713a972
Create Date: 2026-08-03 03:07:04.834070
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "1b7f2fe886a7"
down_revision: Union[str, Sequence[str], None] = "101ae713a972"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "customer_identities",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("tenant_id", sa.String(), nullable=False),
        sa.Column("customer_id", sa.String(), nullable=False),
        sa.Column("provider", sa.String(), nullable=False),
        sa.Column("external_user_id", sa.String(), nullable=False),
        sa.Column("external_chat_id", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
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
        sa.UniqueConstraint(
            "tenant_id",
            "provider",
            "external_user_id",
            name="uq_customer_identity_provider_user",
        ),
    )

    op.create_index(
        op.f("ix_customer_identities_id"),
        "customer_identities",
        ["id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_customer_identities_tenant_id"),
        "customer_identities",
        ["tenant_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_customer_identities_customer_id"),
        "customer_identities",
        ["customer_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_customer_identities_provider"),
        "customer_identities",
        ["provider"],
        unique=False,
    )

    op.create_index(
        op.f("ix_customer_identities_external_user_id"),
        "customer_identities",
        ["external_user_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_customer_identities_external_user_id"),
        table_name="customer_identities",
    )

    op.drop_index(
        op.f("ix_customer_identities_provider"),
        table_name="customer_identities",
    )

    op.drop_index(
        op.f("ix_customer_identities_customer_id"),
        table_name="customer_identities",
    )

    op.drop_index(
        op.f("ix_customer_identities_tenant_id"),
        table_name="customer_identities",
    )

    op.drop_index(
        op.f("ix_customer_identities_id"),
        table_name="customer_identities",
    )

    op.drop_table("customer_identities")
