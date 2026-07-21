from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user
from src.models.saas_core import User, Invoice

from src.domains.invoice.schemas import (
    InvoiceCreate,
    InvoiceResponse,
    InvoiceListResponse,
)

from src.domains.invoice.services.invoice_service import (
    create_invoice,
)


router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"],
)


@router.post(
    "/",
    response_model=InvoiceResponse,
)
async def create_invoice_api(
    data: InvoiceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    return create_invoice(
        db,
        current_user.tenant_id,
        data,
    )



@router.get(
    "/",
    response_model=InvoiceListResponse,
)
async def list_invoices(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    invoices = (
        db.query(Invoice)
        .filter(
            Invoice.tenant_id == current_user.tenant_id
        )
        .order_by(
            Invoice.created_at.desc()
        )
        .all()
    )

    return {
        "invoices": invoices
    }



@router.get(
    "/{invoice_id}",
    response_model=InvoiceResponse,
)
async def get_invoice(
    invoice_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    invoice = (
        db.query(Invoice)
        .filter(
            Invoice.id == invoice_id,
            Invoice.tenant_id == current_user.tenant_id
        )
        .first()
    )

    if not invoice:
        raise HTTPException(
            status_code=404,
            detail="INVOICE_NOT_FOUND"
        )

    return invoice
