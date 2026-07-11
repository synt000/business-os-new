from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user
from src.domains.payment.services.payment_service import create_payment
from src.domains.payment.schemas import PaymentCreate


router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


@router.post("/")
def create_payment_api(
    data: PaymentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    try:
        return create_payment(
            db,
            current_user.tenant_id,
            data
        )

    except Exception as e:

        if str(e) == "DUPLICATE_PAYMENT_NUMBER":
            raise HTTPException(
                status_code=400,
                detail="DUPLICATE_PAYMENT_NUMBER"
            )

        if str(e) == "CUSTOMER_NOT_FOUND":
            raise HTTPException(
                status_code=404,
                detail="CUSTOMER_NOT_FOUND"
            )

        if str(e) == "INVOICE_NOT_FOUND":
            raise HTTPException(
                status_code=404,
                detail="INVOICE_NOT_FOUND"
            )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
