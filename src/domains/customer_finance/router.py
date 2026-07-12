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

from src.domains.customer_finance.services.credit_wallet_service import (
    get_credit_wallet,
    get_credit_history,
    topup_credit,
    refund_credit,
    use_credit_for_invoice
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


@router.get("/{customer_id}/credit")
def customer_credit(
    customer_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_credit_wallet(
        db,
        current_user.tenant_id,
        customer_id
    )


@router.post("/{customer_id}/credit/use")
def use_customer_credit(
    customer_id: str,
    invoice_id: str,
    amount: float,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return use_credit_for_invoice(
        db,
        current_user.tenant_id,
        customer_id,
        invoice_id,
        amount
    )


@router.get("/{customer_id}/credit/history")
def customer_credit_history(
    customer_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_credit_history(
        db,
        current_user.tenant_id,
        customer_id
    )


@router.post("/{customer_id}/credit/topup")
def customer_credit_topup(
    customer_id: str,
    amount: float,
    notes: str = "Manual credit top-up",
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return topup_credit(
        db=db,
        tenant_id=current_user.tenant_id,
        customer_id=customer_id,
        amount=amount,
        notes=notes
    )


@router.post("/{customer_id}/credit/refund")
def customer_credit_refund(
    customer_id: str,
    amount: float,
    invoice_id: str | None = None,
    notes: str = "Credit refund",
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return refund_credit(
        db=db,
        tenant_id=current_user.tenant_id,
       
        customer_id=customer_id,
        amount=amount,
        invoice_id=invoice_id,
        notes=notes
    )

