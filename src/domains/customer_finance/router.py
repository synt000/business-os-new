from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user

from src.domains.customer_finance.services.customer_balance_service import (
    get_customer_balance
)

from src.domains.customer_finance.services.customer_statement_service import (
    get_customer_statement
)


router = APIRouter(
    prefix="/customer-finance",
    tags=["Customer Finance"]
)


@router.get("/{customer_id}/balance")
def customer_balance(
    customer_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_customer_balance(
        db,
        current_user.tenant_id,
        customer_id
    )


@router.get("/{customer_id}/statement")
def customer_statement(
    customer_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_customer_statement(
        db,
        current_user.tenant_id,
        customer_id
    )
