from datetime import datetime

import uuid

def generate_uuid():
    return str(uuid.uuid4())



from sqlalchemy import (
    Column,
    String,
    Boolean,
    Integer,
    Float,
    DateTime,
    ForeignKey,
)

from src.core.database import Base



class BusinessType(Base):
    __tablename__ = "business_types"
    __table_args__ = {"extend_existing": True}

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid
    )

    name = Column(
        String,
        nullable=False,
        unique=True
    )

    code = Column(
        String,
        nullable=False,
        unique=True
    )

    description = Column(
        String,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid
    )

    name = Column(
        String,
        nullable=False
    )

    duration_days = Column(
        Integer,
        nullable=False,
        default=30
    )

    price = Column(
        Float,
        default=0.0
    )

    features_json = Column(
        String,
        nullable=True
    )

    active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class TenantSubscription(Base):
    __tablename__ = "tenant_subscriptions"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid
    )

    tenant_id = Column(
        String,
        ForeignKey("tenants.id"),
        nullable=False
    )

    business_type_id = Column(
        String,
        ForeignKey("business_types.id"),
        nullable=False
    )

    plan_id = Column(
        String,
        ForeignKey("subscription_plans.id"),
        nullable=False
    )

    status = Column(
        String,
        default="ACTIVE"
    )

    start_date = Column(
        DateTime,
        default=datetime.utcnow
    )

    expire_date = Column(
        DateTime,
        nullable=True
    )


# Backward compatibility
# Old registry expects Subscription model


# Backward compatibility for old model registry



class SubscriptionPayment(Base):
    __tablename__ = "subscription_payments"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid
    )

    tenant_id = Column(
        String,
        ForeignKey("tenants.id"),
        nullable=False
    )

    subscription_id = Column(
        String,
        ForeignKey("tenant_subscriptions.id"),
        nullable=False
    )

    amount = Column(
        String,
        default="0"
    )

    status = Column(
        String,
        default="PAID"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# Backward compatibility for activation system

class ActivationKey(Base):
    __tablename__ = "activation_keys"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid
    )

    key = Column(
        String,
        nullable=False,
        unique=True,
        index=True
    )

    tenant_id = Column(
        String,
        ForeignKey("tenants.id"),
        nullable=True
    )

    plan_id = Column(
        String,
        ForeignKey("subscription_plans.id"),
        nullable=True
    )

    status = Column(
        String,
        default="ACTIVE"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# ================================
# SQLAlchemy Backward Compatibility
# ================================
# Legacy models expect class name Subscription

class Subscription(TenantSubscription):
    __tablename__ = "tenant_subscriptions"

    __mapper_args__ = {
        "polymorphic_identity": "subscription",
        "concrete": False
    }

    @property
    def end_date(self):
        return self.expire_date

    @end_date.setter
    def end_date(self, value):
        self.expire_date = value


# Legacy missing models placeholders

try:
    SubscriptionPayment
except NameError:
        id = Column(
            String,
            primary_key=True,
            default=generate_uuid
        )

        tenant_id = Column(
            String,
            ForeignKey("tenants.id"),
            nullable=False
        )

        amount = Column(
            String,
            default="0"
        )

        status = Column(
            String,
            default="PAID"
        )

        created_at = Column(
            DateTime,
            default=datetime.utcnow
        )


try:
    ActivationKey
except NameError:
    class ActivationKey(Base):
        __tablename__ = "activation_keys"

        id = Column(
            String,
            primary_key=True,
            default=generate_uuid
        )

        key = Column(
            String,
            unique=True,
            nullable=False
        )

        active = Column(
            Boolean,
            default=True
        )

        created_at = Column(
            DateTime,
            default=datetime.utcnow
        )




