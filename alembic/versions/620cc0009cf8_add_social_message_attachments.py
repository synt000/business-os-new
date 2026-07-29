"""add social message attachments

Revision ID: 620cc0009cf8
Revises: e35ef3127a9e
Create Date: 2026-07-29 01:40:49.537284

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '620cc0009cf8'
down_revision: Union[str, Sequence[str], None] = 'e35ef3127a9e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "social_messages",
        sa.Column(
            "attachment_url",
            sa.String(),
            nullable=True
        )
    )

    op.add_column(
        "social_messages",
        sa.Column(
            "attachment_name",
            sa.String(),
            nullable=True
        )
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "social_messages",
        "attachment_name"
    )

    op.drop_column(
        "social_messages",
        "attachment_url"
    )
