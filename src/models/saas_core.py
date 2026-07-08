import enum
from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy import Column, String, Boolean, DateTime, Float, ForeignKey, Integer, Enum
from sqlalchemy.orm import relationship, declarative_base

Base = declarativeBase() if 'declarativeBase' in globals() else None
if not Base:
    from sqlalchemy.orm import declarative_base
    Base = declarative_base()

class SubscriptionTier(str, enum.Enum):
    FREE_TRIAL = "FREE_TRIAL"
    STARTUP = "STARTUP"
    BUSINESS = "BUSINESS"
    ENTERPRISE = "ENTERPRISE"

# 1. AUTHENTICATED MASTER USER MODEL (SINGLE ENTRY POINT)
class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(String, default="MEMBER")  # ADMIN, MANAGER, MEMBER
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships mapping
    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    tenant = relationship("Tenant", back_populates="users")

# 2. ISOLATED CORPORATE TENANT MODEL (THE DISPATCHER CORE)
class Tenant(Base):
    __tablename__ = "tenants"
    
    id = Column(String, primary_key=True, index=True)
    company_name = Column(String, nullable=False)
    owner_email = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 3-Day Free Trial Parameters Constraint
    trial_expires_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=3))
    trial_expired = Column(Boolean, default=False)
    
    # Subscription Tiers Status Flags
    subscription_tier = Column(Enum(SubscriptionTier), default=SubscriptionTier.FREE_TRIAL)
    is_billing_active = Column(Boolean, default=True)
    referral_rewards_usd = Column(Float, default=0.0)
    
    # Mapping Arrays
    users = relationship("User", back_populates="tenant", cascade="all, delete-orphan")
    feature_flags = relationship("FeatureFlag", back_populates="tenant", cascade="all, delete-orphan")

# 3. DYNAMIC GRANULAR FEATURE TOGGLES SYSTEM SHARD
class FeatureFlag(Base):
    __tablename__ = "feature_flags"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    feature_name = Column(String, nullable=False)  # e.g., retail_pos, accounting
    enabled = Column(Boolean, default=False)
    
    tenant = relationship("Tenant", back_populates="feature_flags")
