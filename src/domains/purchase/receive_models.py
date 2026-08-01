from sqlalchemy import Column, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from src.core.database import TenantModel


class PurchaseReceive(TenantModel):
    __tablename__ = "purchase_receives"

    purchase_order_id = Column(
        String,
        ForeignKey("purchase_orders.id"),
        nullable=False
    )

    receive_number = Column(
        String,
        nullable=False
    )

    received_date = Column(
        DateTime,
        nullable=True
    )

    received_by = Column(
        String,
        nullable=True
    )

    status = Column(
        String,
        nullable=False,
        default="DRAFT"
    )

    items = relationship(
        "PurchaseReceiveItem",
        back_populates="receive",
        cascade="all, delete-orphan"
    )


class PurchaseReceiveItem(TenantModel):
    __tablename__ = "purchase_receive_items"

    receive_id = Column(
        String,
        ForeignKey("purchase_receives.id"),
        nullable=False
    )

    purchase_item_id = Column(
        String,
        ForeignKey("purchase_items.id"),
        nullable=False
    )

    product_id = Column(
        String,
        ForeignKey("products.id"),
        nullable=False
    )

    quantity_received = Column(
        Numeric,
        nullable=False
    )

    unit_cost = Column(
        Numeric,
        nullable=False
    )

    total_value = Column(
        Numeric,
        nullable=False
    )

    receive = relationship(
        "PurchaseReceive",
        back_populates="items"
    )
