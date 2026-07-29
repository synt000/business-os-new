"""add social message attachments table

Revision ID: 6a02dbec5b87
Revises: 620cc0009cf8
Create Date: 2026-07-29 02:30:10.389968

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a02dbec5b87'
down_revision: Union[str, Sequence[str], None] = '620cc0009cf8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "social_message_attachments",

        sa.Column(
            "id",
            sa.String(),
            primary_key=True
        ),

        sa.Column(
            "message_id",
            sa.String(),
            nullable=False
        ),

        sa.Column(
            "file_url",
            sa.String(),
            nullable=True
        ),

        sa.Column(
            "file_name",
            sa.String(),
            nullable=True
        ),

        sa.Column(
            "file_type",
            sa.String(),
            nullable=True
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
        )
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table(
        "social_message_attachments"
    )
