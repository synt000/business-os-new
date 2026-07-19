from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from src.core.database import Base


class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"

    id = Column(String, primary_key=True)

    name = Column(String, nullable=False)

    duration_days = Column(Integer, nullable=False)

    price = Column(Float, default=0)

    features_json = Column(String, default="{}")

    active = Column(Boolean, default=True)

    created_at = Column(
        DateTime,
        server_default=func.now()
    )


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(String, primary_key=True)

    tenant_id = Column(String, nullable=False)

    plan_id = Column(
        String,
        ForeignKey("subscription_plans.id")
    )

    start_date = Column(DateTime)

    end_date = Column(DateTime)

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
        server_default=func.now()
    )


class SubscriptionPayment(Base):
    __tablename__ = "subscription_payments"

    id = Column(String, primary_key=True)

    tenant_id = Column(String, nullable=False)

    plan_id = Column(
        String,
        nullable=False
    )

    subscription_id = Column(
        String,
        nullable=False
    )

    method = Column(String)

    amount = Column(Float)

    transaction_ref = Column(String)

    status = Column(
        String,
        default="PENDING"
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )


# ======================================
# ACTIVATION KEY MANAGEMENT
# ======================================

class ActivationKey(Base):
    __tablename__ = "activation_keys"

    id = Column(String, primary_key=True)

    key_code = Column(
        String,
        unique=True,
        nullable=False
    )

    plan_id = Column(
        String,
        ForeignKey("subscription_plans.id"),
        nullable=False
    )

    duration_days = Column(
        Integer,
        nullable=False
    )

    used = Column(
        Boolean,
        default=False
    )

    status = Column(
        String,
        default="AVAILABLE"
    )

    tenant_id = Column(
        String,
        nullable=True
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    used_at = Column(
        DateTime,
        nullable=True
    )
