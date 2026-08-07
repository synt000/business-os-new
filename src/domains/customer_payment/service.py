import uuid

from sqlalchemy.orm import Session

from src.models.saas_core import (
    Receivable,
    Customer,
)

from src.domains.customer_payment.models import CustomerPayment

from src.models.saas_core import Invoice

from src.domains.audit.service import AuditService

from src.domains.accounting.services.journal_service import (
    create_customer_payment_journal,
)


def create_customer_payment(
    db: Session,
    tenant_id: str,
    data,
):

    receivable = (
        db.query(Receivable)
        .filter(
            Receivable.id == data.receivable_id,
            Receivable.tenant_id == tenant_id
        )
        .first()
    )

    if not receivable:
        raise Exception("RECEIVABLE_NOT_FOUND")


    if data.amount > receivable.balance_amount:
        raise Exception("PAYMENT_EXCEEDS_BALANCE")


    receivable.paid_amount += data.amount

    receivable.balance_amount = (
        receivable.total_amount -
        receivable.paid_amount
    )


    if receivable.balance_amount <= 0:
        receivable.balance_amount = 0
        receivable.status = "PAID"
    else:
        receivable.status = "PARTIAL"


    payment = CustomerPayment(
        payment_number=data.payment_number,
        customer_id=receivable.customer_id,
        receivable_id=receivable.id,
        amount=data.amount,
        payment_method=data.payment_method,
        status="COMPLETED",
        tenant_id=tenant_id,
    )

    db.add(payment)
    db.flush()


    create_customer_payment_journal(
        db=db,
        tenant_id=tenant_id,
        payment_id=str(payment.id),
        payment_amount=data.amount,
    )


    AuditService.create_audit_log(
        db=db,
        tenant_id=tenant_id,
        action="PAYMENT",
        table_name="customer_payments",
        record_id=str(receivable.id),
        changes=(
            f"amount={data.amount}, "
            f"balance_after={receivable.balance_amount}, "
            f"status={receivable.status}"
        ),
    )


    db.commit()

    return {
        "id": str(payment.id),
        "payment_number": data.payment_number,
        "customer_id": receivable.customer_id,
        "receivable_id": receivable.id,
        "amount": data.amount,
        "payment_method": data.payment_method,
        "status": "COMPLETED",
    }
