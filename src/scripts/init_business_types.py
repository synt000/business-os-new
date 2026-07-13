from src.core.database import Base, engine
from src.models.saas_core import BusinessType

print("=== BUSINESS TYPE INIT ===")

Base.metadata.create_all(bind=engine)

print("✓ Business Type Table Created")
