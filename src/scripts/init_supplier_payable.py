from src.core.database import Base, engine
from src.models.saas_core import SupplierPayable

print("=== SUPPLIER PAYABLE INIT ===")

Base.metadata.create_all(bind=engine)

print("✓ Supplier Payable Tables Created")
