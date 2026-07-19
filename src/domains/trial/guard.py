from datetime import datetime

from sqlalchemy.orm import Session

from src.domains.subscription.models import Subscription


PUBLIC_PATHS = [
    "/login",
    "/register",
    "/token",
    "/docs",
    "/openapi.json",
    "/public",
]


def check_trial_access(
    db: Session,
    tenant_id: str
):

    subscription = (
        db.query(Subscription)
        .filter(
            Subscription.tenant_id == tenant_id,
            Subscription.status == "ACTIVE"
        )
        .first()
    )


    if not subscription:
        return False


    if subscription.end_date:
        if subscription.end_date < datetime.utcnow():
            subscription.status = "EXPIRED"
            db.commit()

            return False


    return True
