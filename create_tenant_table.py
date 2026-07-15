from src.database import engine, Base
from src.domains.tenant.model import Tenant

Base.metadata.create_all(bind=engine)

print("✅ Tenant table created")
