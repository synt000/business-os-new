from src.database import SessionLocal
from src.models.saas_core import BusinessType, BusinessFeature

db = SessionLocal()


features = {

    "ONLINE_SHOP": [
        ("Product Management","product"),
        ("Inventory","inventory"),
        ("Purchase","purchase"),
        ("Sales","sales"),
        ("Customer","customer"),
        ("Invoice","invoice"),
        ("Payment","payment"),
    ],

    "FOOD_BEVERAGE": [
        ("Menu","menu"),
        ("Table Management","table"),
        ("Order","order"),
        ("Kitchen","kitchen"),
        ("Inventory","inventory"),
        ("Supplier","supplier"),
        ("Payment","payment"),
    ],

    "BEAUTY_SALON": [
        ("Service","service"),
        ("Booking","booking"),
        ("Employee","employee"),
        ("Customer History","customer_history"),
        ("Payment","payment"),
    ],

    "RENTAL_SERVICE": [
        ("Rental Item","rental_item"),
        ("Deposit","deposit"),
        ("Rental Payment","rental_payment"),
        ("Return","return"),
        ("Maintenance","maintenance"),
    ],

    "SERVICE_REPAIR": [
        ("Ticket","ticket"),
        ("Job Order","job_order"),
        ("Employee","employee"),
        ("Parts","parts"),
        ("Invoice","invoice"),
    ]
}


for code, items in features.items():

    business = (
        db.query(BusinessType)
        .filter(BusinessType.code == code)
        .first()
    )

    if not business:
        continue


    for name, feature_code in items:

        exists = (
            db.query(BusinessFeature)
            .filter(
                BusinessFeature.business_type_id == business.id,
                BusinessFeature.feature_code == feature_code
            )
            .first()
        )

        if not exists:

            db.add(
                BusinessFeature(
                    business_type_id=business.id,
                    feature_name=name,
                    feature_code=feature_code,
                    enabled=True
                )
            )


db.commit()
db.close()

print("BUSINESS FEATURE SEED COMPLETE")
