from sqlalchemy import inspect
from src.database import engine

inspector = inspect(engine)

tables = inspector.get_table_names()

print("📋 Tables:")
for t in tables:
    print("-", t)

if "tenants" in tables:
    print("\n✅ tenants table exists")
else:
    print("\n❌ tenants table missing")
