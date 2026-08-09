"""add social publish logs

Revision ID: a5e208b5596e
Revises: 38570f4b2539
Create Date: 2026-08-08 00:26:56.559305
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a5e208b5596e"
down_revision: Union[str, Sequence[str], None] = "38570f4b2539"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "social_publish_logs",
        sa.Column(
            "id",
            sa.String(),
            nullable=False
        ),
        sa.Column(
            "post_id",
            sa.String(),
            nullable=False
        ),
        sa.Column(
            "channel_id",
            sa.String(),
            nullable=True
        ),
        sa.Column(
            "platform",
            sa.String(),
            nullable=False
        ),
        sa.Column(
            "success",
            sa.Boolean(),
            nullable=True
        ),
        sa.Column(
            "response",
            sa.Text(),
            nullable=True
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["post_id"],
            ["social_posts.id"],
            ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["channel_id"],
            ["social_channels.id"],
            ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id")
    )

    op.create_index(
        "ix_social_publish_logs_id",
        "social_publish_logs",
        ["id"],
        unique=False
    )

    op.create_index(
        "ix_social_publish_logs_post_id",
        "social_publish_logs",
        ["post_id"],
        unique=False
    )

    op.create_index(
        "ix_social_publish_logs_channel_id",
        "social_publish_logs",
        ["channel_id"],
        unique=False
    )

    op.create_index(
        "ix_social_publish_logs_platform",
        "social_publish_logs",
        ["platform"],
        unique=False
    )


def downgrade() -> None:
    op.drop_index(
        "ix_social_publish_logs_platform",
        table_name="social_publish_logs"
    )

    op.drop_index(
        "ix_social_publish_logs_channel_id",
        table_name="social_publish_logs"
    )

    op.drop_index(
        "ix_social_publish_logs_post_id",
        table_name="social_publish_logs"
    )

    op.drop_index(
        "ix_social_publish_logs_id",
        table_name="social_publish_logs"
    )

    op.drop_table(
        "social_publish_logs"
    )
