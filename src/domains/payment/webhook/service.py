from sqlalchemy.orm import Session

from src.models.saas_core import Payment
from src.domains.payment.webhook.event import WebhookEvent
from src.domains.payment.services.payment_service import sync_invoice_payment_state
from src.domains.payment.services.payment_allocation_service import (
    allocate_completed_payment,
)


def process_webhook_event(
    db: Session,
    event_id: str,
    provider: str,
):
    existing = (
        db.query(WebhookEvent)
        .filter(
            WebhookEvent.event_id == event_id
        )
        .first()
    )

    if existing:
        return {
            "status": "duplicate",
            "event_id": event_id,
        }

    event = WebhookEvent(
        id=event_id,
        event_id=event_id,
        provider=provider,
        processed=False,
    )

    db.add(event)
    db.flush()

    return event



def handle_payment_completed_webhook(
    db: Session,
    tenant_id: str,
    payment_id: str,
    event_id: str,
    provider: str,
):

    try:

        event = process_webhook_event(
            db=db,
            event_id=event_id,
            provider=provider,
        )

        if isinstance(event, dict):
            return event


        payment = (
            db.query(Payment)
            .filter(
                Payment.id == payment_id,
                Payment.tenant_id == tenant_id,
            )
            .first()
        )


        if not payment:
            raise Exception(
                "PAYMENT_NOT_FOUND"
            )


        # ==========================
        # STATE TRANSITION GUARD
        # ==========================

        if payment.status == "COMPLETED":

            event.processed = True
            db.commit()

            return {
                "status": "already_completed",
                "payment_id": payment.id,
            }


        if payment.status != "PENDING":
            raise Exception(
                "INVALID_PAYMENT_STATE"
            )


        # ==========================
        # PAYMENT STATE CHANGE
        # ==========================

        payment.status = "COMPLETED"

        db.flush()


        # ==========================
        # PAYMENT ALLOCATION
        # ==========================

        allocate_completed_payment(
            db=db,
            payment=payment,
            tenant_id=tenant_id,
        )


        # ==========================
        # DOMAIN SYNC
        # ==========================

        sync_invoice_payment_state(
            db=db,
            invoice=payment.invoice,
            tenant_id=tenant_id,
        )


        # ==========================
        # COMPLETE WEBHOOK EVENT
        # ==========================

        event.processed = True


        db.commit()


        return {
            "status": "completed",
            "payment_id": payment.id,
        }


    except Exception:
        db.rollback()
        raise
