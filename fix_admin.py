from uuid import uuid4

from src.core.database import SessionLocal
from src.models.saas_core import Tenant, User
from src.config.security import get_password_hash

db = SessionLocal()

EMAIL = "kokyaw@gmail.com"
PASSWORD = "123456"

tenant = db.query(Tenant).first()

if tenant is None:
    tenant = Tenant(
        id=str(uuid4()),
        company_name="Business OS",
        owner_email=EMAIL,
    )
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    print("Tenant created.")

user = db.query(User).filter(User.email == EMAIL).first()

if user is None:
    user = User(
        id=str(uuid4()),
        email=EMAIL,
        hashed_password=get_password_hash(PASSWORD),
        full_name="Administrator",
        role="ADMIN",
        is_active=True,
        tenant_id=tenant.id,
    )
    db.add(user)
    print("Admin created.")
else:
    user.hashed_password = get_password_hash(PASSWORD)
    user.role = "ADMIN"
    user.is_active = True
    user.tenant_id = tenant.id
    print("Admin updated.")

db.commit()

print("====================================")
print("EMAIL    :", EMAIL)
print("PASSWORD :", PASSWORD)
print("TENANT   :", tenant.id)
print("DONE")
db.close()
