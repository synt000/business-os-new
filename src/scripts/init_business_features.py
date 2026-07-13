from src.core.database import Base, engine

from src.models.saas_core import BusinessFeature


print("=== BUSINESS FEATURE INIT ===")

Base.metadata.create_all(bind=engine)

print("✓ Business Feature Created")
