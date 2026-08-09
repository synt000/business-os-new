"""link social posts to channels

Revision ID: 38570f4b2539
Revises: 411d4f765ae6
Create Date: 2026-08-08 00:17:47.685876

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "38570f4b2539"
down_revision: Union[str, Sequence[str], None] = "411d4f765ae6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "social_posts",
        sa.Column(
            "channel_id",
            sa.String(),
            nullable=True
        )
    )

    op.create_index(
        "ix_social_posts_channel_id",
        "social_posts",
        ["channel_id"],
        unique=False
    )

    op.create_foreign_key(
        "fk_social_posts_channel_id",
        "social_posts",
        "social_channels",
        ["channel_id"],
        ["id"],
        ondelete="CASCADE"
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_social_posts_channel_id",
        "social_posts",
        type_="foreignkey"
    )

    op.drop_index(
        "ix_social_posts_channel_id",
        table_name="social_posts"
    )

    op.drop_column(
        "social_posts",
        "channel_id"
    )
