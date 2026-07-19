from src.core.database import SessionLocal
from src.domains.subscription.models import ActivationKey
from src.domains.subscription.models import SubscriptionPlan
import uuid
import secrets


def create_key():

    db = SessionLocal()

    plan = (
        db.query(SubscriptionPlan)
        .filter(
            SubscriptionPlan.name == "FREE_TRIAL"
        )
        .first()
    )

    if not plan:
        print("PLAN NOT FOUND")
        return

    key = ActivationKey(
        id=str(uuid.uuid4()),
        key_code="ACT-" + secrets.token_hex(4).upper(),
        plan_id=plan.id,
        duration_days=3,
        used=False
    )

    db.add(key)
    db.commit()

    print("NEW KEY:", key.key_code)

    db.close()


if __name__ == "__main__":
    create_key()
