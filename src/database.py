from src.core.database import (
    engine,
    SessionLocal,
    Base,
    get_db,
    TimestampMixin,
    BaseModel,
    TenantModel
)

__all__ = [
    "engine",
    "SessionLocal",
    "Base",
    "get_db",
    "TimestampMixin",
    "BaseModel",
    "TenantModel",
]

# ===== SQLAlchemy MODEL REGISTRY LOAD =====
try:
    from src.domains.inventory.models import Inventory
    from src.domains.movement.models import StockMovement
    from src.domains.product.models import Product
    from src.domains.purchase.models import PurchaseOrder, PurchaseItem
    from src.domains.accounting.models import ProcurementLedger
except Exception as e:
    print("MODEL REGISTRY LOAD ERROR:", e)

