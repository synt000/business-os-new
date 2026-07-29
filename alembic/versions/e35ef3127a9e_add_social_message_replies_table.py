"""add social message replies table

Revision ID: e35ef3127a9e
Revises: dc04d458dcca
Create Date: 2026-07-28 22:17:25.029705

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e35ef3127a9e"
down_revision: Union[str, Sequence[str], None] = "dc04d458dcca"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "social_message_replies",

        sa.Column(
            "id",
            sa.String(),
            primary_key=True
        ),

        sa.Column(
            "message_id",
            sa.String(),
            nullable=False,
            index=True
        ),

        sa.Column(
            "tenant_id",
            sa.String(),
            nullable=False,
            index=True
        ),

        sa.Column(
            "reply_text",
            sa.String(),
            nullable=False
        ),

        sa.Column(
            "replied_by",
            sa.String(),
            nullable=True
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
        "social_message_replies"
    )
