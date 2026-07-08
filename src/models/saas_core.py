import enum
from datetime import datetime, timedelta
from sqlalchemy import Column, String, Boolean, DateTime, Float, ForeignKey, Integer, Enum
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base() if 'declarative_base' in globals() else None
if not Base:
    from sqlalchemy.orm import declarative_base
    Base = declarative_base()

class SubscriptionTier(str, enum.Enum):
    FREE_TRIAL = "FREE_TRIAL"
    STARTUP = "STARTUP"
    BUSINESS = "BUSINESS"
    ENTERPRISE = "ENTERPRISE"

# 1. CORE USER MODEL
class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(String, default="MEMBER")  # ADMIN, MANAGER, MEMBER
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    tenant = relationship("Tenant", back_populates="users")

# 2. CORE TENANT MODEL
class Tenant(Base):
    __tablename__ = "tenants"
    id = Column(String, primary_key=True, index=True)
    company_name = Column(String, nullable=False)
    owner_email = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    trial_expires_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=3))
    trial_expired = Column(Boolean, default=False)
    subscription_tier = Column(Enum(SubscriptionTier), default=SubscriptionTier.FREE_TRIAL)
    is_billing_active = Column(Boolean, default=True)
    referral_rewards_usd = Column(Float, default=0.0)
    
    users = relationship("User", back_populates="tenant", cascade="all, delete-orphan")
    products = relationship("Product", back_populates="tenant", cascade="all, delete-orphan")
    categories = relationship("Category", back_populates="tenant", cascade="all, delete-orphan")

# 3. FIXED ARCHITECTURE: MULTI-TENANT ISOLATED CATEGORY TABLE
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Isolation Boundary Keys
    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    tenant = relationship("Tenant", back_populates="categories")
    products = relationship("Product", back_populates="category")

# 4. FIXED ARCHITECTURE: MULTI-TENANT ISOLATED PRODUCT MODULE TABLE
class Product(Base):
    __tablename__ = "products"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    sku = Column(String, index=True, nullable=False)
    barcode = Column(String, index=True, nullable=True)
    
    # Inventory Stock Metrics
    stock_qty = Column(Integer, default=0)
    purchase_price = Column(Float, default=0.0)
    retail_price = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Isolation Boundary Keys
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    
    tenant = relationship("Tenant", back_populates="products")
    category = relationship("Category", back_populates="products")
