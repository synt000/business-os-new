from sqlalchemy.orm import Session

from src.database import SessionLocal
import importlib

# Load all models before SQLAlchemy mapper initialization
importlib.import_module("src.models.saas_core")

try:
    importlib.import_module("src.models.inventory_models")
except Exception:
    pass

from sqlalchemy.orm import configure_mappers
configure_mappers()

from src.models.saas_core import BusinessType


BUSINESS_TYPES = [
    {
        "name": "Online Shop / E-commerce Seller",
        "code": "ONLINE_SHOP",
        "description": "Online selling, Facebook Shop, TikTok Shop and e-commerce business"
    },
    {
        "name": "2D ဒိုင် / Seller Management",
        "code": "2D_SELLER",
        "description": "2D agent, seller and transaction management"
    },
    {
        "name": "Beauty Salon",
        "code": "BEAUTY_SALON",
        "description": "Beauty salon service and customer management"
    },
    {
        "name": "Food & Beverage",
        "code": "FOOD_BEVERAGE",
        "description": "Restaurant, cafe and food business management"
    },
    {
        "name": "Mini Mart / Retail Shop",
        "code": "MINI_MART",
        "description": "Retail store, inventory and sales management"
    }
]


def seed_business_types(db: Session):
    for item in BUSINESS_TYPES:

        exists = (
            db.query(BusinessType)
            .filter(BusinessType.code == item["code"])
            .first()
        )

        if not exists:
            db.add(
                BusinessType(**item)
            )

    db.commit()


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_business_types(db)
        print("✅ Business Types Seed Completed")
    finally:
        db.close()
