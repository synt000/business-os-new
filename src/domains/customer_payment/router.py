from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user
from src.models.saas_core import User

from src.domains.customer_payment.schemas import (
    CustomerPaymentCreate,
    CustomerPaymentResponse,
)

from src.domains.customer_payment.service import (
    create_customer_payment,
)


router = APIRouter(
    prefix="/customer-payments",
    tags=["Customer Payments"],
)


@router.post(
    "/",
    response_model=CustomerPaymentResponse,
)
def create_payment(
    data: CustomerPaymentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    try:
        return create_customer_payment(
            db,
            current_user.tenant_id,
            data,
        )

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
