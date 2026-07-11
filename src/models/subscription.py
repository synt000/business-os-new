import uuid
from datetime import datetime

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from src.core.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    duration_days = Column(
        Integer,
        nullable=False
    )

    price = Column(
        Float,
        default=0.0
    )

    features_json = Column(
        Text,
        default="{}"
    )

    active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid,
        index=True
    )

    tenant_id = Column(
        String,
        ForeignKey(
            "tenants.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    plan_id = Column(
        String,
        ForeignKey(
            "subscription_plans.id"
        ),
        nullable=False
    )

    start_date = Column(
        DateTime
    )

    end_date = Column(
        DateTime
    )

    status = Column(
        String,
        default="ACTIVE"
    )

    is_trial = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    tenant = relationship(
        "Tenant"
    )

    plan = relationship(
        "SubscriptionPlan"
    )


class SubscriptionPayment(Base):
    __tablename__ = "subscription_payments"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid,
        index=True
    )

    tenant_id = Column(
        String,
        ForeignKey(
            "tenants.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    subscription_id = Column(
        String,
        ForeignKey(
            "subscriptions.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    method = Column(
        String,
        nullable=False
    )

    amount = Column(
        Float,
        default=0.0
    )

    transaction_ref = Column(
        String
    )

    status = Column(
        String,
        default="PENDING"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
