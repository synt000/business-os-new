from src.core.database import SessionLocal
from src.models.saas_core import BusinessType

db = SessionLocal()

print("=== SEED BUSINESS TYPES ===")

businesses = [
    {
        "name": "Online Shop",
        "code": "ONLINE_SHOP",
        "description": "Ecommerce, Orders, Customers, Inventory"
    },
    {
        "name": "2D Seller & Design Service",
        "code": "2D_SELLER",
        "description": "2D Agent, Seller, Logo Design Service"
    },
    {
        "name": "Beauty Salon & Spa",
        "code": "BEAUTY_SALON",
        "description": "Appointment, Service, Customer Management"
    },
    {
        "name": "Mini Mart",
        "code": "MINI_MART",
        "description": "Retail Store, Stock, Purchase, Sales"
    },
    {
        "name": "Repair & Service Shop",
        "code": "SERVICE_REPAIR",
        "description": "Repair Ticket, Customer, Service Tracking"
    }
]


for item in businesses:

    exists = (
        db.query(BusinessType)
        .filter(
            BusinessType.code == item["code"]
        )
        .first()
    )

    if not exists:
        obj = BusinessType(
            name=item["name"],
            code=item["code"],
            description=item["description"]
        )

        db.add(obj)


db.commit()

print("✓ Business Types Seeded")

db.close()
