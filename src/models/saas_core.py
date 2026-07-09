import os
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
import enum

from ..database import Base

class SubscriptionTier(enum.Enum):
    FREE_TRIAL = "FREE_TRIAL"
    STARTUP = "STARTUP"
    BUSINESS = "BUSINESS"
    ENTERPRISE = "ENTERPRISE"

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
    receipts = relationship("BillingReceipt", back_populates="tenant", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="tenant", cascade="all, delete-orphan")
    inventory_ledgers = relationship("InventoryLedger", back_populates="tenant", cascade="all, delete-orphan")
    customers = relationship("Customer", back_populates="tenant", cascade="all, delete-orphan")

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
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")
    inventory_ledgers = relationship("InventoryLedger", back_populates="user", cascade="all, delete-orphan")

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
    inventory_ledgers = relationship("InventoryLedger", back_populates="product", cascade="all, delete-orphan")

# 5. MULTI-TENANT OMNICHANNEL REALTIME ORDERS LOGS
class Order(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, index=True)
    order_number = Column(String, nullable=False, index=True)
    platform_channel = Column(String, nullable=False)
    customer_name = Column(String, nullable=False)
    customer_phone = Column(String, nullable=True)
    total_amount = Column(Float, default=0.0)
    order_status = Column(String, default="PENDING")
    created_at = Column(DateTime, default=datetime.utcnow)

    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    tenant = relationship("Tenant", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(Integer, default=1)
    price_at_sale = Column(Float, nullable=False)

    order_id = Column(String, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    order = relationship("Order", back_populates="items")

    product_id = Column(String, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    product = relationship("Product", back_populates="order_items")

# 6. MULTI-TENANT BILLING RECEIPT STORAGE INGESTION
class BillingReceipt(Base):
    __tablename__ = "billing_receipts"

    id = Column(String, primary_key=True, index=True)
    slip_base64_data = Column(Text, nullable=False)
    verification_status = Column(String, default="PENDING")
    submitted_at = Column(DateTime, default=datetime.utcnow)

    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    tenant = relationship("Tenant", back_populates="receipts")

# 7. MULTI-TENANT SECURITY AUDIT TELEMETRY LOGGING
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    action_type = Column(String, nullable=False)
    module_name = Column(String, nullable=False)
    details_log = Column(Text, nullable=False)
    ip_address = Column(String, default="127.0.0.1")
    logged_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="audit_logs")

    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    tenant = relationship("Tenant", back_populates="audit_logs")

# 8. MULTI-TENANT ADVANCED INVENTORY TRANSACTIONAL LEDGERS
class InventoryLedger(Base):
    __tablename__ = "inventory_ledgers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_type = Column(String, nullable=False)
    quantity_changed = Column(Integer, nullable=False)
    previous_stock = Column(Integer, nullable=False)
    current_stock = Column(Integer, nullable=False)
    reason_note = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    product_id = Column(String, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    product = relationship("Product", back_populates="inventory_ledgers")

    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="inventory_ledgers")

    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    tenant = relationship("Tenant", back_populates="inventory_ledgers")

# ==========================================================================
# PRODUCTION NEW MODEL: MULTI-TENANT CUSTOMERS CRM CORE PROFILE
# ==========================================================================
class Customer(Base):
    __tablename__ = "customers"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    phone = Column(String, nullable=False, index=True)
    email = Column(String, nullable=True)
    address = Column(Text, nullable=True)
    total_spent = Column(Float, default=0.0)                 # Automatically aggregatable metric
    created_at = Column(DateTime, default=datetime.utcnow)

    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    tenant = relationship("Tenant", back_populates="customers")
