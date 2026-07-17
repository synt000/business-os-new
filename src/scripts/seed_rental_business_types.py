from src.core.database import SessionLocal
from src.models.saas_core import BusinessType


db = SessionLocal()


types = [
    ("Online Shop / E-commerce Seller", "ONLINE_SHOP"),
    ("2D ဒိုင် / Seller Management", "2D_SELLER"),
    ("Beauty Salon", "BEAUTY_SALON"),
    ("Food & Beverage", "FOOD_BEVERAGE"),
    ("Mini Mart / Retail Shop", "MINI_MART"),
    ("Rental Service Management", "RENTAL_SERVICE"),
]


for name, code in types:

    exists = (
        db.query(BusinessType)
        .filter(BusinessType.code == code)
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

print("✓ Business Types Seeded")
db.close()
