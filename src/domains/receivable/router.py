from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db

from src.domains.receivable.schemas import (
    ReceivableCreate,
    ReceivablePaymentUpdate,
    ReceivableResponse
)

from src.models.saas_core import (
    Receivable,
    Invoice
)

from src.domains.receivable.services.receivable_service import (
    create_receivable,
    apply_payment_to_receivable
)


router = APIRouter(
    prefix="/receivables",
    tags=["Receivables"]
)


@router.post("/", response_model=ReceivableResponse)
def create_receivable_api(
    data: ReceivableCreate,
    db: Session = Depends(get_db)
):

    invoice = (
        db.query(Invoice)
        .filter(
            Invoice.id == data.invoice_id
        )
        .first()
    )

    if not invoice:
        raise HTTPException(
            status_code=404,
            detail="INVOICE_NOT_FOUND"
        )

    receivable = create_receivable(
        db,
        invoice.tenant_id,
        invoice,
        data.customer_id
    )

    return receivable


@router.post(
    "/{receivable_id}/payment",
    response_model=ReceivableResponse
)
def payment_update(
    receivable_id: str,
    data: ReceivablePaymentUpdate,
    db: Session = Depends(get_db)
):

    receivable = (
        db.query(Receivable)
        .filter(
            Receivable.id == receivable_id
        )
        .first()
    )

    if not receivable:
        raise HTTPException(
            status_code=404,
            detail="RECEIVABLE_NOT_FOUND"
        )

    return apply_payment_to_receivable(
        db,
        receivable,
        data.amount
    )


@router.get(
    "/{receivable_id}",
    response_model=ReceivableResponse
)
def get_receivable(
    receivable_id: str,
    db: Session = Depends(get_db)
):

    receivable = (
        db.query(Receivable)
        .filter(
            Receivable.id == receivable_id
        )
        .first()
    )

    if not receivable:
        raise HTTPException(
            status_code=404,
            detail="RECEIVABLE_NOT_FOUND"
        )

    return receivable
