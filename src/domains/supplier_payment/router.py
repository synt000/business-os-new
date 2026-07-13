from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user

from src.models.saas_core import User

from src.domains.supplier_payment_schemas import (
    SupplierPaymentCreate,
    SupplierPaymentResponse,
)

from src.domains.supplier_payment.service import (
    create_supplier_payment,
)


router = APIRouter(
    prefix="/supplier-payments",
    tags=["Supplier Payments"],
)


@router.post(
    "/",
    response_model=SupplierPaymentResponse,
)
async def create_payment(
    data: SupplierPaymentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    try:
        return create_supplier_payment(
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
