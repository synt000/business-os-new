from datetime import datetime
import uuid

from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    String,
    Float,
    Integer,
    DateTime,
    ForeignKey,
    Index,
)

from src.core.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class AccountLedger(Base):
    __tablename__ = "account_ledgers"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid,
        index=True,
    )

    entry_type = Column(
        String,
        nullable=False,
        index=True,
    )

    account_head = Column(
        String,
        nullable=False,
        index=True,
    )

    amount = Column(
        Float,
        default=0.0,
    )

    reference_id = Column(
        String,
        nullable=True,
        index=True,
    )

    description = Column(
        String,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        index=True,
    )

    tenant_id = Column(
        String,
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
    )

    __table_args__ = (
        Index(
            "idx_ledger_tenant_head",
            "account_head",
            "tenant_id",
        ),
    )


class ProcurementLedger(Base):
    __tablename__ = "procurement_ledgers"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid,
        index=True,
    )

    procurement_number = Column(
        String,
        nullable=False,
        index=True,
    )

    qty_purchased = Column(
        Integer,
        default=1,
    )

    unit_cost = Column(
        Float,
        nullable=False,
    )

    total_cost = Column(
        Float,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        index=True,
    )

    product_id = Column(
        String,
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
    )

    product = relationship(
        "Product",
        back_populates="procurements"
    )

    supplier_id = Column(
        String,
        ForeignKey("suppliers.id", ondelete="CASCADE"),
        nullable=False,
    )

    tenant_id = Column(
        String,
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
    )
