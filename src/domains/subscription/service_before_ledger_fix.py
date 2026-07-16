import uuid
from datetime import datetime, timedelta

from src.domains.subscription.models import (
    SubscriptionPlan,
    Subscription,
    SubscriptionPayment
)


def create_plan(db, data):

    plan = SubscriptionPlan(
        id=data.id,
        name=data.name,
        duration_days=data.duration_days,
        price=data.price,
        features_json=data.features_json
    )

    db.add(plan)
    db.commit()
    db.refresh(plan)

    return plan


def create_subscription(db, tenant_id, plan_id, is_trial=False):

    existing = (
        db.query(Subscription)
        .filter(
            Subscription.tenant_id == tenant_id,
            Subscription.plan_id == plan_id,
            Subscription.status == "ACTIVE"
        )
        .first()
    )

    if existing:
        return existing


    plan = (
        db.query(SubscriptionPlan)
        .filter(
            SubscriptionPlan.id == plan_id
        )
        .first()
    )

    if not plan:
        raise Exception("PLAN_NOT_FOUND")


    days = 7 if is_trial else plan.duration_days


    subscription = Subscription(
        id=str(uuid.uuid4()),
        tenant_id=tenant_id,
        plan_id=plan_id,
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow() + timedelta(days=days),
        status="ACTIVE",
        is_trial=is_trial
    )

    db.add(subscription)
    db.commit()
    db.refresh(subscription)

    return subscription



def create_subscription_payment(db, tenant_id, plan_id, method, transaction_ref=None):

    plan = (
        db.query(SubscriptionPlan)
        .filter(
            SubscriptionPlan.id == plan_id
        )
        .first()
    )

    if not plan:
        raise Exception("PLAN_NOT_FOUND")


    payment = SubscriptionPayment(
        id=str(uuid.uuid4()),
        tenant_id=tenant_id,
        plan_id=plan_id,
        subscription_id="PENDING",
        method=method,
        amount=plan.price,
        transaction_ref=transaction_ref,
        status="PENDING"
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment



def confirm_subscription_payment(db, payment_id):

    payment = (
        db.query(SubscriptionPayment)
        .filter(
            SubscriptionPayment.id == payment_id
        )
        .first()
    )

    if not payment:
        raise Exception("PAYMENT_NOT_FOUND")


    if payment.status == "PAID":
        return payment


    subscription = create_subscription(
        db,
        payment.tenant_id,
        payment.plan_id,
        False
    )

    payment.subscription_id = subscription.id
    payment.status = "PAID"

    db.commit()
    db.refresh(payment)

    return payment
