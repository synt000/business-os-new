from src.core.database import Base, engine
from src.models.saas_core import SupplierPayment

print("=== SUPPLIER PAYMENT INIT ===")

Base.metadata.create_all(bind=engine)

print("✓ Supplier Payment Table Created")
