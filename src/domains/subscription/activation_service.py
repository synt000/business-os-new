from datetime import datetime, timedelta
import uuid

from src.domains.subscription.models import (
    ActivationKey,
    Subscription,
    SubscriptionPlan
)


def activate_key(db, key_code, tenant_id):

    key = (
        db.query(ActivationKey)
        .filter(
            ActivationKey.key_code == key_code
        )
        .first()
    )

    if not key:
        raise Exception("INVALID_KEY")

    if key.status == "REVOKED":
        raise Exception("KEY_REVOKED")

    if key.used:
        raise Exception("KEY_ALREADY_USED")

    if key.status != "AVAILABLE":
        raise Exception("INVALID_KEY_STATUS")


    plan = (
        db.query(SubscriptionPlan)
        .filter(
            SubscriptionPlan.id == key.plan_id
        )
        .first()
    )

    if not plan:
        raise Exception("PLAN_NOT_FOUND")


    now = datetime.utcnow()


    # ==============================
    # CHECK EXISTING SUBSCRIPTION
    # ==============================

    existing = (
        db.query(Subscription)
        .filter(
            Subscription.tenant_id == tenant_id,
            Subscription.status == "ACTIVE"
        )
        .first()
    )


    if existing:

        # Extend existing subscription

        base_date = existing.end_date

        if base_date < now:
            base_date = now

        existing.end_date = (
            base_date +
            timedelta(days=key.duration_days)
        )

        existing.plan_id = plan.id
        existing.is_trial = False

        subscription = existing


    else:

        subscription = Subscription(
            id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            plan_id=plan.id,
            start_date=now,
            end_date=now + timedelta(
                days=key.duration_days
            ),
            status="ACTIVE",
            is_trial=False
        )

        db.add(subscription)


    # ==============================
    # MARK KEY USED
    # ==============================

    key.used = True
    key.tenant_id = tenant_id
    key.used_at = now


    db.commit()
    db.refresh(subscription)

    return subscription
