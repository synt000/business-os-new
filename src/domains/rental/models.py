from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from datetime import datetime

from src.models.saas_core import Base
from src.core.database import TenantModel


class RentalItem(TenantModel):

    __tablename__ = "rental_items"

    item_name = Column(
        String,
        nullable=False
    )

    category = Column(
        String,
        nullable=True
    )

    rate_per_hour = Column(
        Float,
        default=0
    )

    rate_per_day = Column(
        Float,
        default=0
    )

    status = Column(
        String,
        default="AVAILABLE"
    )



class Rental(TenantModel):

    __tablename__ = "rentals"

    customer_id = Column(
        String,
        nullable=True
    )

    item_id = Column(
        String,
        ForeignKey("rental_items.id"),
        nullable=False
    )

    start_time = Column(
        DateTime,
        nullable=False
    )

    end_time = Column(
        DateTime,
        nullable=False
    )

    total_amount = Column(
        Float,
        default=0
    )

    rental_status = Column(
        String,
        default="PENDING"
    )




class RentalCustomer(TenantModel):

    __tablename__ = "rental_customers"

    name = Column(
        String,
        nullable=False
    )

    phone = Column(
        String,
        nullable=True
    )

    address = Column(
        String,
        nullable=True
    )


class RentalPayment(Base):

    __tablename__ = "rental_payments"

    id = Column(
        String,
        primary_key=True,
        default=lambda: __import__("uuid").uuid4().hex
    )

    tenant_id = Column(
        String,
        nullable=False
    )

    rental_id = Column(
        String,
        ForeignKey("rentals.id"),
        nullable=False
    )

    amount_paid = Column(
        Float,
        default=0
    )

    payment_method = Column(
        String
    )

    payment_status = Column(
        String,
        default="PAID"
    )

    paid_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


class RentalDeposit(TenantModel):

    __tablename__ = "rental_deposits"

    rental_id = Column(
        String,
        ForeignKey("rentals.id"),
        nullable=False
    )

    amount = Column(
        Float,
        default=0
    )

    status = Column(
        String,
        default="HELD"
    )

    refund_amount = Column(
        Float,
        default=0
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


class RentalReturn(TenantModel):

    __tablename__ = "rental_returns"

    rental_id = Column(
        String,
        ForeignKey("rentals.id"),
        nullable=False
    )

    returned_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    condition = Column(
        String,
        default="GOOD"
    )

    damage_amount = Column(
        Float,
        default=0
    )

    status = Column(
        String,
        default="RETURNED"
    )


class RentalMaintenance(TenantModel):

    __tablename__ = "rental_maintenance"

    item_id = Column(
        String,
        ForeignKey("rental_items.id"),
        nullable=False
    )

    rental_id = Column(
        String,
        ForeignKey("rentals.id"),
        nullable=True
    )

    issue = Column(
        String,
        nullable=False
    )

    repair_cost = Column(
        Float,
        default=0
    )

    status = Column(
        String,
        default="PENDING"
    )

    completed_at = Column(
        DateTime,
        nullable=True
    )

