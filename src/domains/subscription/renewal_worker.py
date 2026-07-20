from datetime import datetime

from sqlalchemy.orm import Session

from src.domains.subscription.billing_engine import check_expiring_subscriptions
from src.domains.subscription.renewal_service import (
    renewal_health_check,
)


def run_renewal_worker(db: Session):
    """
    Production SaaS Renewal Automation Worker

    Flow:
    Scheduler
        |
        v
    Renewal Worker
        |
        +--> Billing Engine
        |
        +--> Renewal Service
    """

    started_at = datetime.utcnow()

    try:
        expiring = check_expiring_subscriptions(db)

        health = renewal_health_check()

        return {
            "worker": "ONLINE",
            "status": "SUCCESS",
            "started_at": started_at,
            "expiring_subscriptions": expiring,
            "renewal_engine": health,
        }

    except Exception as e:
        return {
            "worker": "FAILED",
            "status": "ERROR",
            "message": str(e),
            "started_at": started_at,
        }


def renewal_worker_health_check():
    return {
        "worker": "ONLINE",
        "mode": "AUTO_RENEWAL_WORKER_READY",
        "timestamp": datetime.utcnow(),
    }
