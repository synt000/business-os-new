from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user
from src.models.saas_core import User

from src.domains.supplier.schemas import (
    SupplierCreate,
    SupplierResponse,
)

from src.domains.supplier.services.supplier_service import (
    create_supplier,
    get_suppliers,
)

router = APIRouter(
    prefix="/suppliers",
    tags=["Suppliers"],
)


@router.post(
    "/",
    response_model=SupplierResponse,
)
async def create_supplier_api(
    data: SupplierCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_supplier(
        db,
        current_user.tenant_id,
        data,
    )


@router.get(
    "/",
    response_model=list[SupplierResponse],
)
async def list_suppliers(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_suppliers(
        db,
        current_user.tenant_id,
    )
