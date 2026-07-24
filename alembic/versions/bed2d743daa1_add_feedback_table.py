"""add feedback table

Revision ID: bed2d743daa1
Revises: f3c552b05d83
Create Date: 2026-07-23
"""

from alembic import op
import sqlalchemy as sa


revision = "bed2d743daa1"
down_revision = "f3c552b05d83"
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        "feedbacks",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True
        ),

        sa.Column(
            "tenant_id",
            sa.String(),
            nullable=False,
            index=True
        ),

        sa.Column(
            "user_id",
            sa.String(),
            nullable=True
        ),

        sa.Column(
            "feedback_type",
            sa.String(),
            nullable=False
        ),

        sa.Column(
            "subject",
            sa.String(),
            nullable=False
        ),

        sa.Column(
            "message",
            sa.Text(),
            nullable=False
        ),

        sa.Column(
            "status",
            sa.String(),
            nullable=True
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=True
        )
    )


def downgrade():

    op.drop_table("feedbacks")
