# Model Registry Loader

from src.models.saas_core import (
    Tenant,
    User,
    Order,
    OrderItem,
    AccountLedger,
    Branch,
    Supplier,
    PurchaseOrder,
    PurchaseItem,
    SupplierPayable,
    SupplierPayment,
    AIInsight,
    AIActionLog,
)

# Load domain models BEFORE Product mapper usage
from src.domains.category.models import Category
from src.domains.product.models import Product
from src.domains.audit.models import AuditLog


__all__ = [
    "Tenant",
    "User",
    "Category",
    "Product",
    "Order",
    "OrderItem",
    "AuditLog",
    "AccountLedger",
    "Branch",
    "Supplier",
    "PurchaseOrder",
    "PurchaseItem",
    "SupplierPayable",
    "SupplierPayment",
    "AIInsight",
    "AIActionLog",
]

from src.models.login_session import LoginSession
