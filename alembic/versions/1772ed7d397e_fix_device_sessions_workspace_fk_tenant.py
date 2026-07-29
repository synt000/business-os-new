"""fix device sessions workspace fk tenant

Revision ID: 1772ed7d397e
Revises: 2464788b7a5f
Create Date: 2026-07-29 22:15:36.613182

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1772ed7d397e'
down_revision: Union[str, Sequence[str], None] = '2464788b7a5f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.drop_constraint(
        "device_sessions_workspace_id_fkey",
        "device_sessions",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "device_sessions_workspace_id_fkey",
        "device_sessions",
        "tenants",
        ["workspace_id"],
        ["id"],
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        "device_sessions_workspace_id_fkey",
        "device_sessions",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "device_sessions_workspace_id_fkey",
        "device_sessions",
        "guest_workspaces",
        ["workspace_id"],
        ["id"],
    )
