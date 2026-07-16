import enum
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Enum, Text, Index
from sqlalchemy.orm import relationship
from src.core.database import Base
from src.domains.inventory import models as inventory_models

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

    business_type_id = Column(
        String,
        ForeignKey("business_types.id"),
        nullable=True
    )

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

    # Login Security Guard Fields
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)
    last_login_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    tenant = relationship("Tenant", back_populates="users")
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")


class Order(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    order_number = Column(String, nullable=False, index=True)
    platform_channel = Column(String, nullable=False)
    customer_name = Column(String, nullable=False)
    customer_phone = Column(String, nullable=True)

    customer_id = Column(
        String,
        ForeignKey("customers.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    total_amount = Column(Float, default=0.0)
    order_status = Column(String, default="PENDING")
    created_at = Column(DateTime, default=datetime.utcnow)

    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    tenant = relationship("Tenant", back_populates="orders")

    customer = relationship(
        "Customer",
        back_populates="orders"
    )

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



class BusinessType(Base):
    __tablename__ = "business_types"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid,
        index=True
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

    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    supplier_name = Column(String, nullable=False, index=True)
    contact_phone = Column(String, nullable=True)

    opening_balance = Column(Float, default=0.0)

    current_balance = Column(Float, default=0.0)

    status = Column(String, default="ACTIVE")

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



class AIBusinessMemory(Base):
    __tablename__ = "ai_business_memory"

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

    memory_type = Column(
        String,
        nullable=False
    )

    content = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )



class AIConversation(Base):
    __tablename__ = "ai_conversations"

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

    user_message = Column(
        String,
        nullable=False
    )

    ai_response = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )



class AIInsight(Base):
    __tablename__ = "ai_insights"

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

    title = Column(
        String,
        nullable=False
    )

    message = Column(
        String,
        nullable=False
    )

    priority = Column(
        String,
        default="NORMAL"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )





class BusinessFeature(Base):
    __tablename__ = "business_features"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid
    )

    business_type_id = Column(
        String,
        ForeignKey("business_types.id"),
        nullable=False
    )

    feature_name = Column(
        String,
        nullable=False
    )

    feature_code = Column(
        String,
        nullable=False
    )

    enabled = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )






class DashboardMenu(Base):
    __tablename__ = "dashboard_menus"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid,
        index=True
    )

    feature_code = Column(
        String,
        nullable=False
    )

    menu_name = Column(
        String,
        nullable=False
    )

    menu_icon = Column(
        String,
        nullable=True
    )

    route_path = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class TenantFeature(Base):
    __tablename__ = "tenant_features"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid,
        index=True
    )

    tenant_id = Column(
        String,
        ForeignKey("tenants.id"),
        nullable=False
    )

    feature_code = Column(
        String,
        nullable=False
    )

    enabled = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


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

    orders = relationship(
        "Order",
        back_populates="customer"
    )


class CustomerCreditWallet(Base):
    __tablename__ = "customer_credit_wallets"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid,
        index=True
    )

    customer_id = Column(
        String,
        ForeignKey("customers.id", ondelete="CASCADE"),
        nullable=False
    )

    credit_amount = Column(
        Float,
        default=0.0
    )

    credit_limit = Column(
        Float,
        default=0.0
    )

    tenant_id = Column(
        String,
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    customer = relationship(
        "Customer"
    )

    tenant = relationship(
        "Tenant"
    )



class CustomerCreditTransaction(Base):
    __tablename__ = "customer_credit_transactions"

    id = Column(String, primary_key=True, default=generate_uuid, index=True)

    customer_id = Column(
        String,
        ForeignKey("customers.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    transaction_type = Column(String, nullable=False)
    amount = Column(Float, default=0.0)

    invoice_id = Column(String, nullable=True, index=True)
    payment_id = Column(String, nullable=True, index=True)

    notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    tenant_id = Column(
        String,
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

   
    customer = relationship("Customer")
    tenant = relationship("Tenant")




class CustomerCreditRiskHistory(Base):
    __tablename__ = "customer_credit_risk_history"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid,
        index=True
    )

    customer_id = Column(
        String,
        ForeignKey("customers.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    credit_score = Column(
        Integer,
        default=0
    )

    risk_level = Column(
        String,
        nullable=False
    )

    credit_balance = Column(
        Float,
        default=0.0
    )

    credit_limit = Column(
        Float,
        default=0.0
    )

    calculated_at = Column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )

    tenant_id = Column(
        String,
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    customer = relationship("Customer")
    tenant = relationship("Tenant")


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


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid,
        index=True
    )

    invoice_number = Column(
        String,
        nullable=False,
        index=True
    )

    amount = Column(
        Float,
        default=0.0
    )

    status = Column(
        String,
        default="UNPAID"
    )


    order_id = Column(
        String,
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=True
    )

    order = relationship(
        "Order"
    )

    tenant_id = Column(
        String,
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False
    )

    tenant = relationship(
        "Tenant"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class Payment(Base):
    __tablename__ = "payments"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid,
        index=True
    )

    payment_number = Column(
        String,
        nullable=False,
        index=True
    )

    amount = Column(
        Float,
        nullable=False
    )

    payment_method = Column(
        String,
        nullable=False
    )

    status = Column(
        String,
        default="COMPLETED"
    )

    invoice_id = Column(
        String,
        ForeignKey("invoices.id", ondelete="CASCADE"),
        nullable=False
    )

    invoice = relationship(
        "Invoice"
    )

    tenant_id = Column(
        String,
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False
    )

    tenant = relationship(
        "Tenant"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class Receivable(Base):
    __tablename__ = "receivables"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid,
        index=True
    )

    customer_id = Column(
        String,
        ForeignKey("customers.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    invoice_id = Column(
        String,
        ForeignKey("invoices.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    total_amount = Column(
        Float,
        nullable=False,
        default=0.0
    )

    paid_amount = Column(
        Float,
        default=0.0
    )

    balance_amount = Column(
        Float,
        default=0.0
    )

    status = Column(
        String,
        default="OPEN"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    customer = relationship(
        "Customer"
    )

    invoice = relationship(
        "Invoice"
    )

    tenant_id = Column(
        String,
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False
    )

    tenant = relationship(
        "Tenant"
    )


class CustomerCreditActionHistory(Base):

    __tablename__ = "customer_credit_action_history"


    id = Column(
        String,
        primary_key=True,
        default=generate_uuid,
        index=True
    )


    customer_id = Column(
        String,
        ForeignKey("customers.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )


    action = Column(
        String,
        nullable=False
    )


    old_limit = Column(
        Float,
        default=0.0
    )


    new_limit = Column(
        Float,
        default=0.0
    )


   
    reason = Column(
        String,
        nullable=True
    )

    credit_score = Column(
        Integer,
        default=0
    )

    behavior_score = Column
    behavior_score = Column(
        Integer,
        default=0
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )

    tenant_id = Column(
        String,
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    customer = relationship("Customer")
    tenant = relationship("Tenant")


class CustomerCreditAlert(Base):

    __tablename__ = "customer_credit_alerts"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid,
        index=True
    )

    customer_id = Column(
        String,
        ForeignKey("customers.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    tenant_id = Column(
        String,
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    alert_type = Column(
        String,
        nullable=False
    )

    severity = Column(
        String,
        default="WARNING"
    )

    message = Column(
        String,
        nullable=False
    )

    status = Column(
        String,
        default="OPEN"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )


    customer = relationship("Customer")

    tenant = relationship("Tenant")



class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid,
        index=True
    )

    purchase_number = Column(
        String,
        nullable=False,
        index=True
    )

    supplier_id = Column(
        String,
        ForeignKey("suppliers.id"),
        nullable=False
    )

    total_amount = Column(
        Float,
        default=0.0
    )

    status = Column(
        String,
        default="DRAFT"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    tenant_id = Column(
        String,
        ForeignKey("tenants.id"),
        nullable=False
    )




class SupplierPayable(Base):
    __tablename__ = "supplier_payables"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid,
        index=True
    )

    purchase_order_id = Column(
        String,
        ForeignKey("purchase_orders.id"),
        nullable=False
    )

    supplier_id = Column(
        String,
        ForeignKey("suppliers.id"),
        nullable=False
    )

    total_amount = Column(
        Float,
        default=0.0
    )

    paid_amount = Column(
        Float,
        default=0.0
    )

    balance_amount = Column(
        Float,
        default=0.0
    )

    status = Column(
        String,
        default="OPEN"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    tenant_id = Column(
        String,
        ForeignKey("tenants.id"),
        nullable=False
    )


class PurchaseItem(Base):
    __tablename__ = "purchase_items"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid,
        index=True
    )

    purchase_order_id = Column(
        String,
        ForeignKey("purchase_orders.id"),
        nullable=False
    )

    product_id = Column(
        String,
        ForeignKey("products.id"),
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    unit_cost = Column(
        Float,
        nullable=False
    )

    total_cost = Column(
        Float,
        nullable=False
    )

    tenant_id = Column(
        String,
        ForeignKey("tenants.id"),
        nullable=False
    )



class SupplierPayment(Base):
    __tablename__ = "supplier_payments"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid,
        index=True
    )

    payment_number = Column(
        String,
        nullable=False,
        index=True
    )

    supplier_id = Column(
        String,
        ForeignKey("suppliers.id"),
        nullable=False
    )

    payable_id = Column(
        String,
        ForeignKey("supplier_payables.id"),
        nullable=False
    )

    amount = Column(
        Float,
        nullable=False
    )

    payment_method = Column(
        String,
        default="CASH"
    )

    status = Column(
        String,
        default="COMPLETED"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    tenant_id = Column(
        String,
        ForeignKey("tenants.id"),
        nullable=False
    )


class BusinessProfile(Base):

    __tablename__ = "business_profiles"


    id = Column(
        String,
        primary_key=True,
        default=generate_uuid,
        index=True
    )


    business_name = Column(
        String,
        nullable=False
    )


    logo_url = Column(
        String,
        nullable=True
    )


    phone = Column(
        String,
        nullable=True
    )


    address = Column(
        String,
        nullable=True
    )


    description = Column(
        String,
        nullable=True
    )


    tenant_id = Column(
        String,
        ForeignKey("tenants.id"),
        nullable=False
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )



class SocialAccount(Base):

    __tablename__ = "social_accounts"


    id = Column(
        String,
        primary_key=True,
        default=generate_uuid,
        index=True
    )


    platform = Column(
        String,
        nullable=False
    )


    account_name = Column(
        String,
        nullable=True
    )


    account_url = Column(
        String,
        nullable=True
    )


    access_token = Column(
        String,
        nullable=True
    )


    status = Column(
        String,
        default="CONNECTED"
    )


    tenant_id = Column(
        String,
        ForeignKey("tenants.id"),
        nullable=False
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )



class SocialMessage(Base):
    __tablename__ = "social_messages"

    id = Column(String, primary_key=True)

    platform = Column(String, nullable=False)

    customer_name = Column(String)

    customer_id = Column(String)

    message = Column(String)

    message_type = Column(String, default="TEXT")

    status = Column(String, default="NEW")

    reply_text = Column(String)

    tenant_id = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)


class Employee(Base):
    __tablename__ = "employees"

    id = Column(
        String,
        primary_key=True
    )

    employee_code = Column(
        String,
        nullable=False
    )

    full_name = Column(
        String,
        nullable=False
    )

    phone = Column(
        String,
        nullable=True
    )

    email = Column(
        String,
        nullable=True
    )

    department = Column(
        String,
        nullable=True
    )

    position = Column(
        String,
        nullable=True
    )

    hire_date = Column(
        DateTime,
        nullable=True
    )

    salary = Column(
        Float,
        default=0
    )

    status = Column(
        String,
        default="ACTIVE"
    )

    tenant_id = Column(
        String,
        ForeignKey("tenants.id"),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
