import enum
from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Enum,
)

from sqlalchemy.orm import relationship

from src.database import Base


class SubscriptionTier(str, enum.Enum):
    FREE_TRIAL = "FREE_TRIAL"
    STARTUP = "STARTUP"
    BUSINESS = "BUSINESS"
    ENTERPRISE = "ENTERPRISE"


# 1. AUTHENTICATED MASTER USER MODEL
class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(String, default="MEMBER")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    tenant_id = Column(
        String,
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
    )

    tenant = relationship("Tenant", back_populates="users")


# 2. TENANT MODEL
class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(String, primary_key=True, index=True)
    company_name = Column(String, nullable=False)
    owner_email = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    trial_expires_at = Column(
        DateTime,
        default=lambda: datetime.utcnow() + timedelta(days=3),
    )
    trial_expired = Column(Boolean, default=False)

    subscription_tier = Column(
        Enum(SubscriptionTier),
        default=SubscriptionTier.FREE_TRIAL,
    )

    is_billing_active = Column(Boolean, default=True)
    referral_rewards_usd = Column(Float, default=0.0)

    users = relationship(
        "User",
        back_populates="tenant",
        cascade="all, delete-orphan",
    )

    feature_flags = relationship(
        "FeatureFlag",
        back_populates="tenant",
        cascade="all, delete-orphan",
    )


# 3. FEATURE FLAG MODEL
class FeatureFlag(Base):
    __tablename__ = "feature_flags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(
        String,
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
    )
    feature_name = Column(String, nullable=False)
    enabled = Column(Boolean, default=False)

    tenant = relationship("Tenant", back_populates="feature_flags")
