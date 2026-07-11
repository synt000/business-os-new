import enum
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Enum, Text, Index
from sqlalchemy.orm import relationship
from src.core.database import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

class SubscriptionTier(enum.Enum):
    FREE_TRIAL = "FREE_TRIAL"
    STARTUP = "STARTUP"
    BUSINESS = "BUSINESS"
    ENTERPRISE = "ENTERPRISE"

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    company_name = Column(String, nullable=False)
    owner_email = Column(String, nullable=False)
    subscription_tier = Column(Enum(SubscriptionTier), default=SubscriptionTier.FREE_TRIAL)
    is_billing_active = Column(Boolean, default=True)
    trial_expired = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    max_sku_limit = Column(Integer, default=50)
    max_order_limit = Column(Integer, default=100)
    enable_pos_feature = Column(Boolean, default=True)
    enable_ai_forecast = Column(Boolean, default=False)

    users = relationship("User", back_populates="tenant", cascade="all, delete-orphan")
    products = relationship("Product", back_populates="tenant", cascade="all, delete-orphan")
    categories = relationship("Category", back_populates="tenant", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="tenant", cascade="all, delete-orphan")
    receipts = relationship("BillingReceipt", back_populates="tenant", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="tenant", cascade="all, delete-orphan")
    account_ledgers = relationship("AccountLedger", back_populates="tenant", cascade="all, delete-orphan")
    branches = relationship("Branch", back_populates="tenant", cascade="all, delete-orphan")
    suppliers = relationship("Supplier", back_populates="tenant", cascade="all, delete-orphan")
    procurements = relationship("ProcurementLedger", back_populates="tenant", cascade="all, delete-orphan")
    customers = relationship("Customer", back_populates="tenant", cascade="all, delete-orphan")
    invitations = relationship("WorkspaceInvitation", back_populates="tenant", cascade="all, delete-orphan")

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(String, default="MEMBER")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    tenant = relationship("Tenant", back_populates="users")
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    tenant = relationship("Tenant", back_populates="categories")

class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, default=generate_uuid, index=True)
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
    procurements = relationship("ProcurementLedger", back_populates="product", cascade="all, delete-orphan")

class Order(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, default=generate_uuid, index=True)
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

class BillingReceipt(Base):
    __tablename__ = "billing_receipts"

    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    slip_base64_data = Column(Text, nullable=False)
    verification_status = Column(String, default="PENDING")
    submitted_at = Column(DateTime, default=datetime.utcnow)

    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    tenant = relationship("Tenant", back_populates="receipts")

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    action_type = Column(String, nullable=False, index=True)
    module_name = Column(String, nullable=False, index=True)
    details_log = Column(Text, nullable=False)
    ip_address = Column(String, default="127.0.0.1")
    logged_at = Column(DateTime, default=datetime.utcnow, index=True)

    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="audit_logs")
    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    tenant = relationship("Tenant", back_populates="audit_logs")

class AccountLedger(Base):
    __tablename__ = "account_ledgers"

    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    entry_type = Column(String, nullable=False, index=True)
    account_head = Column(String, nullable=False, index=True)
    amount = Column(Float, default=0.0)
    reference_id = Column(String, nullable=True, index=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    tenant = relationship("Tenant", back_populates="account_ledgers")

    __table_args__ = (Index("idx_ledger_tenant_head", "account_head", "tenant_id"),)

class Branch(Base):
    __tablename__ = "branches"

    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    branch_name = Column(String, nullable=False, index=True)
    location_address = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    tenant = relationship("Tenant", back_populates="branches")

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    supplier_name = Column(String, nullable=False, index=True)
    contact_phone = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    tenant = relationship("Tenant", back_populates="suppliers")
    procurements = relationship("ProcurementLedger", back_populates="supplier", cascade="all, delete-orphan")

class ProcurementLedger(Base):
    __tablename__ = "procurement_ledgers"

    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    procurement_number = Column(String, nullable=False, index=True)
    qty_purchased = Column(Integer, default=1)
    unit_cost = Column(Float, nullable=False)
    total_cost = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    product_id = Column(String, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    product = relationship("Product", back_populates="procurements")
    supplier_id = Column(String, ForeignKey("suppliers.id", ondelete="CASCADE"), nullable=False)
    supplier = relationship("Supplier", back_populates="procurements")
    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    tenant = relationship("Tenant", back_populates="procurements")

class Customer(Base):
    __tablename__ = "customers"

    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    customer_name = Column(String, nullable=False, index=True)
    customer_email = Column(String, nullable=True, index=True)
    customer_phone = Column(String, nullable=True, index=True)
    total_spent = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    tenant = relationship("Tenant", back_populates="customers")

class WorkspaceInvitation(Base):
    __tablename__ = "workspace_invitations"

    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    invite_email = Column(String, nullable=False, index=True)
    target_role = Column(String, default="MEMBER")
    invitation_token = Column(String, unique=True, index=True)
    is_accepted = Column(Boolean, default=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    tenant = relationship("Tenant", back_populates="invitations")
