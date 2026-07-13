from src.core.database import SessionLocal

from src.models.saas_core import (
    BusinessType,
    BusinessFeature,
)


db = SessionLocal()


features = {


"ONLINE_SHOP":[
"PRODUCT",
"ORDER",
"CUSTOMER_CHAT",
"INVENTORY",
"DELIVERY",
"PROMOTION",
"SOCIAL_MEDIA"
],


"2D_SELLER":[
"2D_MANAGEMENT",
"CUSTOMER",
"PAYMENT",
"DESIGN_SERVICE",
"FILE_DELIVERY",
"LOG_HISTORY"
],


"RESTAURANT":[
"MENU",
"TABLE",
"KITCHEN",
"ORDER",
"DELIVERY",
"DAILY_SALES"
],


"BEAUTY_SALON":[
"BOOKING",
"CUSTOMER_HISTORY",
"STAFF",
"SERVICE_PACKAGE",
"PAYMENT"
],


"MINI_MART":[
"POS",
"PRODUCT",
"PURCHASE",
"SUPPLIER",
"INVENTORY",
"DEBT"
]

}


for code, items in features.items():

    business = (
        db.query(BusinessType)
        .filter(
            BusinessType.code == code
        )
        .first()
    )


    if not business:
        continue


    for item in items:

        exists = (
            db.query(BusinessFeature)
            .filter(
                BusinessFeature.business_type_id == business.id,
                BusinessFeature.feature_code == item
            )
            .first()
        )


        if not exists:

            db.add(
                BusinessFeature(
                    business_type_id=business.id,
                    feature_name=item,
                    feature_code=item
                )
            )


db.commit()

print("✓ Features Seeded")

db.close()
