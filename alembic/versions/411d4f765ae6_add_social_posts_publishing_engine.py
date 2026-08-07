"""add social posts publishing engine

Revision ID: 411d4f765ae6
Revises: 3efc24b95335
Create Date: 2026-08-08 00:03:03.210596

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "411d4f765ae6"
down_revision: Union[str, Sequence[str], None] = "3efc24b95335"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "social_posts",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("tenant_id", sa.String(), nullable=False),
        sa.Column("platform", sa.String(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("media_url", sa.Text(), nullable=True),
        sa.Column("status", sa.String(), nullable=True),
        sa.Column("scheduled_at", sa.DateTime(), nullable=True),
        sa.Column("published_at", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.String(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenants.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_social_posts_id",
        "social_posts",
        ["id"],
        unique=False,
    )

    op.create_index(
        "ix_social_posts_platform",
        "social_posts",
        ["platform"],
        unique=False,
    )

    op.create_index(
        "ix_social_posts_status",
        "social_posts",
        ["status"],
        unique=False,
    )

    op.create_index(
        "ix_social_posts_tenant_id",
        "social_posts",
        ["tenant_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_social_posts_tenant_id",
        table_name="social_posts",
    )

    op.drop_index(
        "ix_social_posts_status",
        table_name="social_posts",
    )

    op.drop_index(
        "ix_social_posts_platform",
        table_name="social_posts",
    )

    op.drop_index(
        "ix_social_posts_id",
        table_name="social_posts",
    )

    op.drop_table("social_posts")
