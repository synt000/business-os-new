"""add social channels table

Revision ID: cad94677c363
Revises: 260989671c4d
Create Date: 2026-07-28

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "cad94677c363"

down_revision: Union[str, Sequence[str], None] = "260989671c4d"

branch_labels: Union[str, Sequence[str], None] = None

depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:

    op.create_table(
        "social_channels",

        sa.Column(
            "id",
            sa.String(),
            primary_key=True,
            nullable=False
        ),

        sa.Column(
            "tenant_id",
            sa.String(),
            sa.ForeignKey(
                "tenants.id",
                ondelete="CASCADE"
            ),
            nullable=False
        ),

        sa.Column(
            "platform",
            sa.String(),
            nullable=False
        ),

        sa.Column(
            "channel_name",
            sa.String(),
            nullable=True
        ),

        sa.Column(
            "external_id",
            sa.String(),
            nullable=True
        ),

        sa.Column(
            "access_token",
            sa.Text(),
            nullable=True
        ),

        sa.Column(
            "webhook_token",
            sa.String(),
            nullable=True
        ),

        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=True,
            server_default=sa.text("true")
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=True
        )
    )


    op.create_index(
        "ix_social_channels_id",
        "social_channels",
        ["id"]
    )


    op.create_index(
        "ix_social_channels_tenant_id",
        "social_channels",
        ["tenant_id"]
    )


    op.create_index(
        "ix_social_channels_platform",
        "social_channels",
        ["platform"]
    )


    op.create_index(
        "ix_social_channels_external_id",
        "social_channels",
        ["external_id"]
    )



def downgrade() -> None:

    op.drop_index(
        "ix_social_channels_external_id",
        table_name="social_channels"
    )

    op.drop_index(
        "ix_social_channels_platform",
        table_name="social_channels"
    )

    op.drop_index(
        "ix_social_channels_tenant_id",
        table_name="social_channels"
    )

    op.drop_index(
        "ix_social_channels_id",
        table_name="social_channels"
    )

    op.drop_table(
        "social_channels"
    )
