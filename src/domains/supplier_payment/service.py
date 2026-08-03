import uuid

from sqlalchemy.orm import Session

from src.domains.accounting.services.journal_service import (
    create_supplier_payment_journal,
)

from src.domains.purchase.models import SupplierPayment

from src.domains.purchase.models import SupplierPayable
from src.models.saas_core import (
    Supplier,
)
from src.domains.accounting.models import AccountLedger
from src.domains.audit.service import AuditService


def create_supplier_payment(
    db: Session,
    tenant_id: str,
    data,
):

    payable = (
        db.query(SupplierPayable)
        .filter(
            SupplierPayable.id == data.payable_id,
            SupplierPayable.tenant_id == tenant_id
        )
        .first()
    )

    if not payable:
        raise Exception("PAYABLE_NOT_FOUND")


    if data.amount > payable.balance_amount:
        raise Exception("PAYMENT_EXCEEDS_BALANCE")


    payment = SupplierPayment(
        id=str(uuid.uuid4()),
        payment_number=data.payment_number,
        supplier_id=payable.supplier_id,
        payable_id=payable.id,
        amount=data.amount,
        payment_method=data.payment_method,
        status="COMPLETED",
        tenant_id=tenant_id,
    )


    db.add(payment)


    create_supplier_payment_journal(
        db=db,
        tenant_id=tenant_id,
        payment_id=payment.id,
        payment_amount=data.amount,
    )

    payable.paid_amount += data.amount

    supplier = (
        db.query(Supplier)
        .filter(
            Supplier.id == payable.supplier_id,
            Supplier.tenant_id == tenant_id
        )
        .first()
    )

    if supplier:
        supplier.current_balance -= data.amount


    payable.balance_amount = (
        payable.total_amount -
        payable.paid_amount
    )


    if payable.balance_amount <= 0:
        payable.balance_amount = 0
        payable.status = "PAID"

    else:
        payable.status = "PARTIAL"


    AuditService.create_audit_log(
        db=db,
        tenant_id=tenant_id,
        action="PAYMENT",
        table_name="supplier_payments",
        record_id=str(payment.id),
        changes=(
            f"payable_id={payable.id}, "
            f"amount={data.amount}, "
            f"payment_method={data.payment_method}, "
            f"balance_after={payable.balance_amount}"
        ),
    )

    db.commit()
    db.refresh(payment)


    return payment
