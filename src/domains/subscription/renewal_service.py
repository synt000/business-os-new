import uuid

from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from src.domains.subscription.models import (
    Subscription,
    SubscriptionPayment,
    SubscriptionPlan
)


def find_renewal_candidates(
    db: Session,
    days_before: int = 7
):
    """
    Find subscriptions near expiry
    """

    limit = datetime.utcnow() + timedelta(
        days=days_before
    )

    subscriptions = (
        db.query(Subscription)
        .filter(
            Subscription.status == "ACTIVE",
            Subscription.end_date <= limit
        )
        .all()
    )

    return subscriptions



def create_renewal_payment(
    db: Session,
    subscription_id: str,
    method="KBZPAY"
):
    """
    Create renewal payment request
    """

    subscription = (
        db.query(Subscription)
        .filter(
            Subscription.id == subscription_id
        )
        .first()
    )


    if not subscription:
        raise Exception(
            "SUBSCRIPTION_NOT_FOUND"
        )


    plan = (
        db.query(SubscriptionPlan)
        .filter(
            SubscriptionPlan.id == subscription.plan_id
        )
        .first()
    )


    if not plan:
        raise Exception(
            "PLAN_NOT_FOUND"
        )


    payment = SubscriptionPayment(
        id=str(uuid.uuid4()),
        tenant_id=subscription.tenant_id,
        plan_id=plan.id,
        subscription_id=subscription.id,
        method=method,
        amount=plan.price,
        status="PENDING"
    )


    db.add(payment)
    db.commit()
    db.refresh(payment)


    return payment



def renew_subscription(
    db: Session,
    subscription_id: str
):
    """
    Extend subscription after payment
    """

    subscription = (
        db.query(Subscription)
        .filter(
            Subscription.id == subscription_id
        )
        .first()
    )


    if not subscription:
        raise Exception(
            "SUBSCRIPTION_NOT_FOUND"
        )


    plan = (
        db.query(SubscriptionPlan)
        .filter(
            SubscriptionPlan.id == subscription.plan_id
        )
        .first()
    )


    subscription.start_date = datetime.utcnow()

    subscription.end_date = (
        datetime.utcnow()
        +
        timedelta(
            days=plan.duration_days
        )
    )

    subscription.status = "ACTIVE"


    db.commit()
    db.refresh(subscription)


    return subscription



def renewal_health_check():

    return {
        "renewal_engine": "ONLINE",
        "mode": "AUTO_RENEWAL_READY",
        "timestamp": datetime.utcnow()
    }
