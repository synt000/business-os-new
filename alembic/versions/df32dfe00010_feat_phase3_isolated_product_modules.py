"""feat_phase3_isolated_product_modules"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = "df32dfe00010"
down_revision: Union[str, Sequence[str], None] = "2f3a86ca41c7"
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table(
        "products",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("product_name", sa.String(), nullable=False),
        sa.Column("sku", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("price", sa.Float(), default=0),
        sa.Column("stock_quantity", sa.Integer(), default=0),
        sa.Column("tenant_id", sa.String(), nullable=False),

        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenants.id"],
            ondelete="CASCADE"
        )
    )


def downgrade() -> None:
    op.drop_table("products")
