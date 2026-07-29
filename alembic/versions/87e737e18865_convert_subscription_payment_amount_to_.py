"""convert subscription payment amount to float

Revision ID: 87e737e18865
Revises: f33f29cd5201
Create Date: 2026-07-29 18:15:52.822962

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '87e737e18865'
down_revision: Union[str, Sequence[str], None] = 'f33f29cd5201'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "subscription_payments",
        "amount",
        existing_type=sa.String(),
        type_=sa.Float(),
        existing_nullable=True,
        postgresql_using="amount::double precision",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "subscription_payments",
        "amount",
        existing_type=sa.Float(),
        type_=sa.String(),
        existing_nullable=True,
    )
