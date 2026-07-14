import uuid

from sqlalchemy.orm import Session

from src.domains.accounting.services.journal_service import (
    create_supplier_payment_journal,
)

from src.models.saas_core import (
    SupplierPayment,
    SupplierPayable,
    Supplier,
    AccountLedger,
)


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


    db.commit()
    db.refresh(payment)


    return payment
