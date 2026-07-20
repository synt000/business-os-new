from sqlalchemy.orm import Session

from src.domains.rental.models import (
    Rental,
    RentalPayment,
)
from src.domains.accounting.models import AccountLedger

from src.models.saas_core import (
    Invoice,
)


def create_rental_payment(
    db: Session,
    tenant_id: str,
    rental_id: str,
    amount: float,
    payment_method: str = None,
):

    rental = (
        db.query(Rental)
        .filter(
            Rental.id == rental_id,
            Rental.tenant_id == tenant_id
        )
        .first()
    )

    if not rental:
        raise Exception("RENTAL_NOT_FOUND")


    payment = RentalPayment(
        tenant_id=tenant_id,
        rental_id=rental_id,
        amount_paid=amount,
        payment_method=payment_method,
        payment_status="PAID",
    )


    invoice = Invoice(
        invoice_number=f"RENTAL-{rental_id[:8]}",
        amount=amount,
        status="PAID",
        tenant_id=tenant_id,
    )


    db.add(invoice)
    db.flush()


    ledger = AccountLedger(
        entry_type="INCOME",
        account_head="RENTAL_PAYMENT",
        amount=amount,
        reference_id=invoice.id,
        description="Rental payment received",
        tenant_id=tenant_id,
    )


    db.add(payment)
    db.add(ledger)

    db.commit()

    db.refresh(payment)

    return payment
