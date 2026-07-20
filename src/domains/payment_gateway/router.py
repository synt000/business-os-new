from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.database import get_db

from src.domains.payment_gateway.service import (
    PaymentGatewayService
)

from src.domains.subscription.service import (
    confirm_subscription_payment
)


router = APIRouter(
    prefix="/payment-gateway",
    tags=["Payment Gateway"]
)



@router.post("/webhook/{provider}")
def payment_webhook(
    provider: str,
    payload: dict,
    db: Session = Depends(get_db)
):

    payment_id = payload.get(
        "payment_id"
    )


    if not payment_id:
        raise HTTPException(
            status_code=400,
            detail="PAYMENT_ID_REQUIRED"
        )


    verify = PaymentGatewayService.verify_payment(
        provider,
        payload
    )


    if not verify.get("verified"):

        raise HTTPException(
            status_code=400,
            detail="PAYMENT_VERIFY_FAILED"
        )


    payment = confirm_subscription_payment(
        db,
        payment_id
    )


    return {

        "status": "SUCCESS",

        "provider": provider,

        "payment_id": payment.id,

        "subscription_id":
            payment.subscription_id
    }

