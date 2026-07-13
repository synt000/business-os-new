from src.core.database import Base, engine
from src.models.saas_core import TenantFeature

print("=== TENANT FEATURES INIT ===")

Base.metadata.create_all(bind=engine)

print("✓ Tenant Feature Table Created")
