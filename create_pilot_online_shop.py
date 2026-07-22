from src.models import *
from src.core.database import SessionLocal
from src.core.security import get_password_hash
import uuid


db = SessionLocal()


company_name = "WarWar Online Shop Demo"
email = "pilot@warwarshop.com"
password = "Pilot@12345"

business_type_id = "b4ccf596-9928-4d4f-9d82-6304b4e3f7fe"


# check existing
existing = db.query(User).filter(
    User.email == email
).first()

if existing:
    print("Already exists")
    exit()


tenant = Tenant(
    id=str(uuid.uuid4()),
    company_name=company_name,
    owner_email=email,
    subscription_tier="FREE_TRIAL",
    is_billing_active=True,
    trial_expired=False,
    business_type_id=business_type_id
)

db.add(tenant)
db.flush()


user = User(
    id=str(uuid.uuid4()),
    email=email,
    hashed_password=get_password_hash(password),
    full_name="WarWar Owner",
    role="OWNER",
    is_active=True,
    tenant_id=tenant.id
)

db.add(user)

db.commit()


print("=== PILOT CREATED ===")
print("Tenant:", tenant.id)
print("Email:", email)
print("Password:", password)
