from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user

from src.models.saas_core import User

from src.domains.bank_reconciliation.models import (
    BankTransaction,
)

from src.domains.bank_reconciliation.schemas import (
    BankTransactionCreate,
)

from src.domains.bank_reconciliation.service import (
    match_bank_transaction,
)

from src.domains.audit.service import AuditService


router = APIRouter(
    prefix="/bank-reconciliation",
    tags=["Bank Reconciliation"],
)


@router.post("/transactions")
def create_bank_transaction(
    data: BankTransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    if data.external_reference:

        existing = (
            db.query(BankTransaction)
            .filter(
                BankTransaction.tenant_id == current_user.tenant_id,
                BankTransaction.bank_name == data.bank_name,
                BankTransaction.external_reference == data.external_reference,
            )
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=409,
                detail="DUPLICATE_BANK_TRANSACTION",
            )

    transaction = BankTransaction(
        tenant_id=current_user.tenant_id,
        bank_name=data.bank_name,
        account_number=data.account_number,
        transaction_date=data.transaction_date,
        external_reference=data.external_reference,
        description=data.description,
        amount=data.amount,
        direction=data.direction,
        status="UNMATCHED",
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    AuditService.create_audit_log(
        db=db,
        tenant_id=current_user.tenant_id,
        action="BANK_TRANSACTION_CREATED",
        table_name="bank_transactions",
        record_id=transaction.id,
        changes=(
            f"Bank transaction created: "
            f"{transaction.bank_name} "
            f"{transaction.amount}"
        ),
        user_id=current_user.id,
    )

    db.commit()

    return transaction



@router.post("/transactions/{transaction_id}/match")
def match_transaction(
    transaction_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    transaction = (
        db.query(BankTransaction)
        .filter(
            BankTransaction.id == transaction_id,
            BankTransaction.tenant_id == current_user.tenant_id,
        )
        .first()
    )

    if not transaction:
        raise HTTPException(
            status_code=404,
            detail="BANK_TRANSACTION_NOT_FOUND",
        )


    return match_bank_transaction(
        db=db,
        bank_transaction=transaction,
        tenant_id=current_user.tenant_id,
    )


@router.get("/transactions")
def list_bank_transactions(
    status: str | None = None,
    bank_name: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    query = (
        db.query(BankTransaction)
        .filter(
            BankTransaction.tenant_id == current_user.tenant_id
        )
    )

    if status:
        query = query.filter(
            BankTransaction.status == status.upper()
        )

    if bank_name:
        query = query.filter(
            BankTransaction.bank_name == bank_name
        )

    transactions = (
        query
        .order_by(
            BankTransaction.created_at.desc()
        )
        .all()
    )

    return {
        "total": len(transactions),
        "items": transactions,
    }


@router.get("/summary")
def bank_reconciliation_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    base = (
        db.query(BankTransaction)
        .filter(
            BankTransaction.tenant_id == current_user.tenant_id
        )
    )

    total = base.count()

    matched = (
        base.filter(
            BankTransaction.status == "MATCHED"
        )
        .count()
    )

    unmatched = (
        base.filter(
            BankTransaction.status == "UNMATCHED"
        )
        .count()
    )

    credit = (
        db.query(
            func.sum(BankTransaction.amount)
        )
        .filter(
            BankTransaction.tenant_id == current_user.tenant_id,
            BankTransaction.direction == "CREDIT",
        )
        .scalar()
        or 0
    )

    debit = (
        db.query(
            func.sum(BankTransaction.amount)
        )
        .filter(
            BankTransaction.tenant_id == current_user.tenant_id,
            BankTransaction.direction == "DEBIT",
        )
        .scalar()
        or 0
    )

    return {
        "total_transactions": total,
        "matched": matched,
        "unmatched": unmatched,
        "total_credit": credit,
        "total_debit": debit,
    }

