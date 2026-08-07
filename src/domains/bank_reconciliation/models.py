from datetime import datetime
import uuid

from sqlalchemy import (
    Column,
    String,
    Float,
    DateTime,
    ForeignKey,
    Index,
)

from src.core.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class BankTransaction(Base):

    __tablename__ = "bank_transactions"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid,
        index=True,
    )

    tenant_id = Column(
        String,
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    bank_name = Column(
        String,
        nullable=False,
    )

    account_number = Column(
        String,
        nullable=True,
    )

    transaction_date = Column(
        DateTime,
        nullable=False,
    )

    external_reference = Column(
        String,
        nullable=True,
        index=True,
    )

    description = Column(
        String,
        nullable=True,
    )

    amount = Column(
        Float,
        nullable=False,
    )

    direction = Column(
        String,
        nullable=False,
    )

    match_confidence = Column(
        Float,
        nullable=True,
    )

    match_reason = Column(
        String,
        nullable=True,
    )

    matched_at = Column(
        DateTime,
        nullable=True,
    )

    matched_payment_id = Column(
        String,
        nullable=True,
        index=True,
    )

    status = Column(
        String,
        nullable=False,
        default="UNMATCHED",
        index=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        index=True,
    )

    __table_args__ = (
        Index(
            "idx_bank_tx_tenant_status",
            "tenant_id",
            "status",
        ),
    )
