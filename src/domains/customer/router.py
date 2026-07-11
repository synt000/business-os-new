from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user
from src.models.saas_core import User

from src.domains.customer.schemas import (
    CustomerCreate,
    CustomerResponse,
)

from src.domains.customer.services.customer_service import (
    create_customer,
    get_customers,
)

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@router.post(
    "/",
    response_model=CustomerResponse,
)
async def create_customer_api(
    data: CustomerCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_customer(
        db,
        current_user.tenant_id,
        data,
    )


@router.get(
    "/",
    response_model=list[CustomerResponse],
)
async def list_customers(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_customers(
        db,
        current_user.tenant_id,
    )
