from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user
from src.models.saas_core import User

from src.domains.invoice.schemas import (
    InvoiceCreate,
    InvoiceResponse,
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
