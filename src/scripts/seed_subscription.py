from src.core.database import SessionLocal
from src.domains.subscription.models import SubscriptionPlan
import uuid
import json


def seed_plans():

    db = SessionLocal()

    plans = [
        {
            "name": "FREE_TRIAL",
            "duration_days": 3,
            "price": 0,
            "features_json": json.dumps({
                "features": [
                    "PRODUCT",
                    "ORDER",
                    "CUSTOMER"
                ]
            })
        },
        {
            "name": "STARTER",
            "duration_days": 30,
            "price": 10,
            "features_json": json.dumps({
                "features": [
                    "PRODUCT",
                    "ORDER",
                    "CUSTOMER",
                    "REPORT"
                ]
            })
        },
        {
            "name": "BUSINESS",
            "duration_days": 90,
            "price": 25,
            "features_json": json.dumps({
                "features": [
                    "PRODUCT",
                    "ORDER",
                    "CUSTOMER",
                    "INVENTORY",
                    "PAYMENT",
                    "AI_ASSISTANT",
                    "AI_INSIGHT"
                ]
            })
        },
        {
            "name": "ENTERPRISE",
            "duration_days": 360,
            "price": 100,
            "features_json": json.dumps({
                "features": [
                    "ALL_MODULES",
                    "AI_ASSISTANT",
                    "AI_INSIGHT",
                    "API",
                    "WHITE_LABEL"
                ]
            })
        }
    ]


    for p in plans:

        exists = (
            db.query(SubscriptionPlan)
            .filter(
                SubscriptionPlan.name == p["name"]
            )
            .first()
        )

        if exists:
            continue

        plan = SubscriptionPlan(
            id=str(uuid.uuid4()),
            **p
        )

        db.add(plan)

    db.commit()
    db.close()

    print("SUBSCRIPTION PLANS SEEDED")


if __name__ == "__main__":
    seed_plans()
