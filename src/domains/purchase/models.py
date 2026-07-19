from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Float,
    Integer,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from src.core.database import Base
from src.models.saas_core import generate_uuid


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid,
        index=True
    )

    purchase_number = Column(
        String,
        nullable=False,
        index=True
    )

    supplier_id = Column(
        String,
        ForeignKey("suppliers.id"),
        nullable=False
    )

    total_amount = Column(
        Float,
        default=0.0
    )

    status = Column(
        String,
        default="DRAFT"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    tenant_id = Column(
        String,
        ForeignKey("tenants.id"),
        nullable=False
    )


class SupplierPayable(Base):
    __tablename__ = "supplier_payables"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid,
        index=True
    )

    purchase_order_id = Column(
        String,
        ForeignKey("purchase_orders.id"),
        nullable=False
    )

    supplier_id = Column(
        String,
        ForeignKey("suppliers.id"),
        nullable=False
    )

    total_amount = Column(
        Float,
        default=0.0
    )

    paid_amount = Column(
        Float,
        default=0.0
    )

    balance_amount = Column(
        Float,
        default=0.0
    )

    status = Column(
        String,
        default="OPEN"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    tenant_id = Column(
        String,
        ForeignKey("tenants.id"),
        nullable=False
    )


class PurchaseItem(Base):
    __tablename__ = "purchase_items"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid,
        index=True
    )

    purchase_order_id = Column(
        String,
        ForeignKey("purchase_orders.id"),
        nullable=False
    )

    product_id = Column(
        String,
        ForeignKey("products.id"),
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    unit_cost = Column(
        Float,
        nullable=False
    )

    total_cost = Column(
        Float,
        nullable=False
    )

    tenant_id = Column(
        String,
        ForeignKey("tenants.id"),
        nullable=False
    )


class SupplierPayment(Base):
    __tablename__ = "supplier_payments"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid,
        index=True
    )

    payment_number = Column(
        String,
        nullable=False,
        index=True
    )

    supplier_id = Column(
        String,
        ForeignKey("suppliers.id"),
        nullable=False
    )

    payable_id = Column(
        String,
        ForeignKey("supplier_payables.id"),
        nullable=False
    )

    amount = Column(
        Float,
        nullable=False
    )

    payment_method = Column(
        String,
        default="CASH"
    )

    status = Column(
        String,
        default="COMPLETED"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    tenant_id = Column(
        String,
        ForeignKey("tenants.id"),
        nullable=False
    )
