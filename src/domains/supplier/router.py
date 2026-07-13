from fastapi import APIRouter, Depends, HTTPException
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
    list_suppliers,
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
    try:
        return create_supplier(
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


@router.get("/")
async def get_suppliers(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return list_suppliers(
        db,
        current_user.tenant_id,
    )
