import os
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from ..database import Base

class SubscriptionTier(enum.Enum):
    FREE_TRIAL = "FREE_TRIAL"
    STARTUP = "STARTUP"
    BUSINESS = "BUSINESS"
    ENTERPRISE = "ENTERPRISE"

class UserRole(enum.Enum):
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    MEMBER = "MEMBER"

# 1. B2B SAAS WORKSPACE TENANT MATRIX
class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(String, primary_key=True, index=True)
    company_name = Column(String, nullable=False)
    owner_email = Column(String, nullable=False)
    subscription_tier = Column(Enum(SubscriptionTier), default=SubscriptionTier.FREE_TRIAL)
    is_billing_active = Column(Boolean, default=True)
    trial_expired = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Core Backlink Relationships
    users = relationship("User", back_populates="tenant", cascade="all, delete-orphan")
    products = relationship("Product", back_populates="tenant", cascade="all, delete-orphan")
    categories = relationship("Category", back_populates="tenant", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="tenant", cascade="all, delete-orphan")

# 2. HARDENED ENTERPRISE SAAS MASTER USER SCHEMAS
class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(String, default="MEMBER")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    tenant = relationship("Tenant", back_populates="users")

# 3. MULTI-TENANT ISOLATED STOCK CATEGORY MATRIX
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    tenant = relationship("Tenant", back_populates="categories")

# 4. AUTHORITATIVE CENTRAL B2B INVENTORY CORE PRODUCT
class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    sku = Column(String, nullable=False, index=True)
    barcode = Column(String, nullable=True)
    stock_qty = Column(Integer, default=0)
    purchase_price = Column(Float, default=0.0)
    retail_price = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    tenant = relationship("Tenant", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product", cascade="all, delete-orphan")

# ==========================================================================
# NEXT SPRINT NEW MODEL: MULTI-TENANT OMNICHANNEL REALTIME ORDERS LOGS
# ==========================================================================
class Order(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, index=True)
    order_number = Column(String, nullable=False, index=True)  # E.g., ORD-2026-0001
    platform_channel = Column(String, nullable=False)         # Facebook, TikTok, WhatsApp, Telegram
    customer_name = Column(String, nullable=False)
    customer_phone = Column(String, nullable=True)
    total_amount = Column(Float, default=0.0)
    order_status = Column(String, default="PENDING")          # PENDING, PROCESSING, DELIVERED, CANCELLED
    created_at = Column(DateTime, default=datetime.utcnow)

    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    tenant = relationship("Tenant", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(Integer, default=1)
    price_at_sale = Column(Float, nullable=False)  # Preserves physical receipt matrix histories

    order_id = Column(String, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    order = relationship("Order", back_populates="items")

    product_id = Column(String, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    product = relationship("Product", back_populates="order_items")
