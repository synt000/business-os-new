"""add customer leads table

Revision ID: 260989671c4d
Revises: ca29e8a066e0
Create Date: 2026-07-28 20:44:33.208399

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "260989671c4d"
down_revision: Union[str, Sequence[str], None] = "ca29e8a066e0"
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table(
        "customer_leads",

        sa.Column(
            "id",
            sa.String(),
            primary_key=True,
            nullable=False
        ),

        sa.Column(
            "tenant_id",
            sa.String(),
            nullable=False
        ),

        sa.Column(
            "customer_name",
            sa.String(),
            nullable=False
        ),

        sa.Column(
            "customer_phone",
            sa.String(),
            nullable=True
        ),

        sa.Column(
            "product_id",
            sa.String(),
            nullable=True
        ),

        sa.Column(
            "quantity",
            sa.Integer(),
            nullable=True,
            server_default="1"
        ),

        sa.Column(
            "message",
            sa.Text(),
            nullable=True
        ),

        sa.Column(
            "source",
            sa.String(),
            nullable=True,
            server_default="website"
        ),

        sa.Column(
            "status",
            sa.String(),
            nullable=True,
            server_default="NEW"
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=True
        ),

        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenants.id"],
            ondelete="CASCADE"
        )
    )


    op.create_index(
        "ix_customer_leads_id",
        "customer_leads",
        ["id"]
    )


    op.create_index(
        "ix_customer_leads_tenant_id",
        "customer_leads",
        ["tenant_id"]
    )


    op.create_index(
        "ix_customer_leads_product_id",
        "customer_leads",
        ["product_id"]
    )


    op.create_index(
        "ix_customer_leads_created_at",
        "customer_leads",
        ["created_at"]
    )


def downgrade() -> None:

    op.drop_index(
        "ix_customer_leads_created_at",
        table_name="customer_leads"
    )

    op.drop_index(
        "ix_customer_leads_product_id",
        table_name="customer_leads"
    )

    op.drop_index(
        "ix_customer_leads_tenant_id",
        table_name="customer_leads"
    )

    op.drop_index(
        "ix_customer_leads_id",
        table_name="customer_leads"
    )

    op.drop_table(
        "customer_leads"
    )
