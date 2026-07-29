from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.database import get_db

from .schemas import PaymentWebhookPayload
from .service import handle_payment_completed_webhook


router = APIRouter(
    prefix="/payment",
    tags=["Payment Webhook"],
)


@router.post("/webhook")
def payment_webhook(
    payload: PaymentWebhookPayload,
    db: Session = Depends(get_db),
):

    result = handle_payment_completed_webhook(
        db=db,
        tenant_id=payload.tenant_id,
        payment_id=payload.payment_id,
        event_id=payload.event_id,
        provider=payload.provider,
    )

    return result
