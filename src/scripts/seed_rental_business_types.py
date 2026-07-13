from src.core.database import SessionLocal
from src.models.saas_core import BusinessType


db = SessionLocal()


types = [
    ("Online Shop","ONLINE_SHOP"),
    ("2D Seller + Design Studio","2D_DESIGN"),
    ("Restaurant Cafe","RESTAURANT"),
    ("Beauty Salon","BEAUTY_SALON"),
    ("Wholesale Distribution","WHOLESALE"),
]


for name,code in types:

    exists = (
        db.query(BusinessType)
        .filter(BusinessType.code==code)
        .first()
    )

    if not exists:
        db.add(
            BusinessType(
                name=name,
                code=code
            )
        )


db.commit()

print("✓ Rental Business Types Seeded")
