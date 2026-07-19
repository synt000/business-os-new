import uuid
from datetime import datetime, timedelta

from src.domains.subscription.feature_sync import sync_plan_features_to_tenant
from src.domains.subscription.models import (
    SubscriptionPlan,
    Subscription,
    SubscriptionPayment
)

from src.models.saas_core import AccountLedger, Invoice


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

    sync_plan_features_to_tenant(
        db,
        tenant_id,
        plan_id
    )

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


    if transaction_ref:
        existing_payment = (
            db.query(SubscriptionPayment)
            .filter(
                SubscriptionPayment.transaction_ref == transaction_ref
            )
            .first()
        )

        if existing_payment:
            raise Exception("DUPLICATE_TRANSACTION_REFERENCE")


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

    cash_ledger = AccountLedger(
        entry_type="DEBIT",
        account_head="CASH_ASSET",
        amount=payment.amount,
        reference_id=payment.id,
        description=f"Cash received for subscription {payment.plan_id}",
        tenant_id=payment.tenant_id
    )

    revenue_ledger = AccountLedger(
        entry_type="CREDIT",
        account_head="SUBSCRIPTION_REVENUE",
        amount=payment.amount,
        reference_id=payment.id,
        description=f"Subscription revenue {payment.plan_id}",
        tenant_id=payment.tenant_id
    )

    db.add(cash_ledger)
    db.add(revenue_ledger)

    invoice = Invoice(
        id=str(uuid.uuid4()),
        invoice_number=f"SUB-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        amount=payment.amount,
        status="PAID",
        order_id=subscription.id,
        tenant_id=payment.tenant_id
    )

    db.add(invoice)

    db.commit()
    db.refresh(payment)

    return payment
