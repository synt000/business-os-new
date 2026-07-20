from datetime import datetime

from sqlalchemy.orm import Session

from src.domains.subscription.models import Subscription
from src.domains.subscription.renewal_worker import (
    run_renewal_worker,
)


def expire_subscriptions(db: Session):
    """
    Expire subscriptions that passed end_date.
    """

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



def run_subscription_scheduler(db: Session):
    """
    Production SaaS Subscription Scheduler

    Daily Automation Flow:

    1. Expire old subscriptions
    2. Scan renewal candidates
    3. Trigger renewal worker
    """

    started_at = datetime.utcnow()

    try:

        expired_count = expire_subscriptions(db)

        renewal_result = run_renewal_worker(db)

        return {
            "scheduler": "ONLINE",
            "status": "SUCCESS",
            "started_at": started_at,
            "expired_subscriptions": expired_count,
            "renewal_worker": renewal_result,
        }

    except Exception as e:

        return {
            "scheduler": "FAILED",
            "status": "ERROR",
            "message": str(e),
            "started_at": started_at,
        }



def scheduler_health_check():

    return {
        "scheduler": "ONLINE",
        "mode": "DAILY_RENEWAL_AUTOMATION_READY",
        "timestamp": datetime.utcnow(),
    }
