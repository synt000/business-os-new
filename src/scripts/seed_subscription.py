from datetime import datetime
from src.core.database import SessionLocal

# Load Core ORM Models First
from src.models.saas_core import Tenant, User

# Load Subscription Models
from src.domains.subscription.models import SubscriptionPlan

import uuid


def seed_plans():

    db = SessionLocal()

    plans = [
        {
            "name": "FREE_TRIAL",
            "duration_days": 3,
            "price": 0,
            "features_json": '{"orders":true,"products":true}'
        },
        {
            "name": "STARTER",
            "duration_days": 30,
            "price": 10,
            "features_json": '{"orders":true,"products":true,"reports":true}'
        },
        {
            "name": "BUSINESS",
            "duration_days": 90,
            "price": 25,
            "features_json": '{"all_modules":true}'
        },
        {
            "name": "ENTERPRISE",
            "duration_days": 360,
            "price": 100,
            "features_json": '{"white_label":true,"api":true}'
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

        if not exists:

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
