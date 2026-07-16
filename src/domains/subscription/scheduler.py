from datetime import datetime
from sqlalchemy.orm import Session

from src.domains.subscription.models import Subscription


def expire_subscriptions(db: Session):
    now = datetime.utcnow()

    subscriptions = (
        db.query(Subscription)
        .filter(
            Subscription.status == "ACTIVE",
            Subscription.end_date < now
        )
        .all()
    )

    count = 0

    for sub in subscriptions:
        sub.status = "EXPIRED"
        count += 1

    if count:
        db.commit()

    return count
