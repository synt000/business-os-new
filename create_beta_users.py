from src.core.database import SessionLocal
from src.models.saas_core import User
from src.core.security import get_password_hash


db = SessionLocal()


TENANT_ID = "26d8a1b8-889b-4ba7-91db-57df91a406b3"


users = [
    {
        "email": "beta.sales@businessos.com",
        "password": "Beta12345!",
        "name": "Beta Sales",
        "role": "SALES"
    },
    {
        "email": "beta.inventory@businessos.com",
        "password": "Beta12345!",
        "name": "Beta Inventory",
        "role": "INVENTORY"
    },
    {
        "email": "beta.accounting@businessos.com",
        "password": "Beta12345!",
        "name": "Beta Accounting",
        "role": "ACCOUNTANT"
    },
    {
        "email": "beta.manager@businessos.com",
        "password": "Beta12345!",
        "name": "Beta Manager",
        "role": "MANAGER"
    },
    {
        "email": "beta.viewer@businessos.com",
        "password": "Beta12345!",
        "name": "Beta Viewer",
        "role": "VIEWER"
    }
]


for u in users:

    exists = (
        db.query(User)
        .filter(User.email == u["email"])
        .first()
    )

    if exists:
        print("EXISTS:", u["email"])
        continue


    user = User(
        email=u["email"],
        hashed_password=get_password_hash(u["password"]),
        full_name=u["name"],
        role=u["role"],
        tenant_id=TENANT_ID,
        is_active=True
    )

    db.add(user)

    print(
        "CREATED:",
        u["email"],
        u["role"]
    )


db.commit()

db.close()

print("Beta users ready")
