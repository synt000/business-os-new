from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user
from src.core.permissions.guard import require_permission
from src.domains.payment.services.payment_service import create_payment, get_payments
from src.domains.payment.services.payment_config_service import get_available_payment_methods
from src.domains.payment.services.payment_config_write_service import (
    enable_payment_method,
    disable_payment_method,
    set_default_payment_method,
)
from src.domains.payment.schemas import (
    PaymentCreate,
    PaymentMethodConfigResponse,
    PaymentConfigUpdateRequest,
)


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


@router.get("/list")
def list_payments(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_payments(
        db,
        current_user.tenant_id
    )


@router.get("/methods", response_model=list[PaymentMethodConfigResponse])
def list_payment_methods(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_available_payment_methods(
        db,
        current_user.tenant_id
    )

@router.post("/config/enable")
def enable_payment_config(
    data: PaymentConfigUpdateRequest,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("payment_config.manage")),
):
    return enable_payment_method(
        db,
        current_user.tenant_id,
        data.payment_code,
    )


@router.post("/config/disable")
def disable_payment_config(
    data: PaymentConfigUpdateRequest,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("payment_config.manage")),
):
    return disable_payment_method(
        db,
        current_user.tenant_id,
        data.payment_code,
    )


@router.post("/config/default")
def default_payment_config(
    data: PaymentConfigUpdateRequest,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("payment_config.manage")),
):
    return set_default_payment_method(
        db,
        current_user.tenant_id,
        data.payment_code,
    )
