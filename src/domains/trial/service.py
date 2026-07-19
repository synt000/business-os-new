from datetime import datetime, timedelta
import uuid

from sqlalchemy.orm import Session

from src.domains.subscription.models import (
    Subscription,
    SubscriptionPlan
)


TRIAL_DAYS = 7


def create_trial_subscription(
    db: Session,
    tenant_id: str
):
    """
    Create FREE TRIAL subscription for new tenant
    """

    existing = (
        db.query(Subscription)
        .filter(
            Subscription.tenant_id == tenant_id,
            Subscription.status == "ACTIVE"
        )
        .first()
    )

    if existing:
        return existing


    trial_plan = (
        db.query(SubscriptionPlan)
        .filter(
            SubscriptionPlan.name == "FREE_TRIAL"
        )
        .first()
    )


    if not trial_plan:
        raise Exception(
            "FREE_TRIAL_PLAN_NOT_FOUND"
        )


    subscription = Subscription(
        id=str(uuid.uuid4()),
        tenant_id=tenant_id,
        plan_id=trial_plan.id,
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow()
        + timedelta(days=TRIAL_DAYS),
        status="ACTIVE",
        is_trial=True
    )


    db.add(subscription)
    db.commit()
    db.refresh(subscription)

    return subscription



def get_trial_status(
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
        return {
            "active": False,
            "message": "NO_SUBSCRIPTION"
        }


    remaining = (
        subscription.end_date -
        datetime.utcnow()
    ).days


    if remaining <= 0:
        subscription.status = "EXPIRED"
        db.commit()

        return {
            "active": False,
            "expired": True,
            "message": "TRIAL_EXPIRED"
        }


    return {
        "active": True,
        "is_trial": subscription.is_trial,
        "days_left": remaining,
        "end_date": str(
            subscription.end_date
        )
    }
