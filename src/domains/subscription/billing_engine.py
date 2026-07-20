from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from src.domains.subscription.models import Subscription
from src.models.saas_core import Invoice


def check_expiring_subscriptions(
    db: Session,
    days_before: int = 7
):
    """
    Production SaaS Billing Reminder Engine

    Flow:
    ACTIVE Subscription
        |
        v
    Expiry Detection
        |
        v
    Renewal Invoice Generation
    """

    now = datetime.utcnow()
    limit = now + timedelta(days=days_before)

    expiring = (
        db.query(Subscription)
        .filter(
            Subscription.status == "ACTIVE",
            Subscription.end_date <= limit,
            Subscription.end_date >= now
        )
        .all()
    )

    created = 0

    for sub in expiring:

        exists = (
            db.query(Invoice)
            .filter(
                Invoice.order_id == sub.id,
                Invoice.status == "PENDING"
            )
            .first()
        )

        if exists:
            continue


        invoice = Invoice(
            id=f"SUB-INV-{sub.id}",
            invoice_number=f"RENEW-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            amount=0,
            status="PENDING",
            order_id=sub.id,
            tenant_id=sub.tenant_id
        )


        db.add(invoice)

        created += 1


    if created:
        db.commit()


    return {
        "checked": len(expiring),
        "renewal_invoices_created": created,
        "timestamp": datetime.utcnow()
    }



def billing_health_check(db: Session):

    active = (
        db.query(Subscription)
        .filter(
            Subscription.status == "ACTIVE"
        )
        .count()
    )

    expired = (
        db.query(Subscription)
        .filter(
            Subscription.status == "EXPIRED"
        )
        .count()
    )


    return {
        "active_subscriptions": active,
        "expired_subscriptions": expired,
        "billing_engine": "ONLINE"
    }
