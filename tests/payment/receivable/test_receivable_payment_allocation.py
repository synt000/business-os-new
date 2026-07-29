import uuid
from src.models.saas_core import (
    Receivable,
    Payment,
    Invoice,
    Customer,
)


def create_test_customer(db_session, tenant_id):

    customer = Customer(
        id=str(uuid.uuid4()),
        customer_name="Test Customer",
        tenant_id=tenant_id,
    )

    db_session.add(customer)
    db_session.commit()

    return customer.id



def test_receivable_partial_payment_allocation(
    db_session,
    tenant_id,
    invoice_id,
):

    customer_id = create_test_customer(
        db_session,
        tenant_id,
    )

    invoice = (
        db_session.query(Invoice)
        .filter(
            Invoice.id == invoice_id
        )
        .first()
    )


    receivable = Receivable(
        customer_id=customer_id,
        invoice_id=invoice.id,
        total_amount=1000,
        paid_amount=0,
        balance_amount=1000,
        status="OPEN",
        tenant_id=tenant_id,
    )

    db_session.add(receivable)


    payment = Payment(
        payment_number="REC-PARTIAL-001",
        amount=300,
        payment_method="TEST",
        status="COMPLETED",
        invoice_id=invoice.id,
        tenant_id=tenant_id,
    )

    db_session.add(payment)

    db_session.commit()


    receivable.paid_amount += 300
    receivable.balance_amount = (
        receivable.total_amount -
        receivable.paid_amount
    )

    receivable.status = "PARTIAL"

    db_session.commit()


    assert receivable.paid_amount == 300
    assert receivable.balance_amount == 700
    assert receivable.status == "PARTIAL"



def test_receivable_full_payment_allocation(
    db_session,
    tenant_id,
    invoice_id,
):

    customer_id = create_test_customer(
        db_session,
        tenant_id,
    )

    invoice = (
        db_session.query(Invoice)
        .filter(
            Invoice.id == invoice_id
        )
        .first()
    )


    receivable = Receivable(
        customer_id=customer_id,
        invoice_id=invoice.id,
        total_amount=1000,
        paid_amount=0,
        balance_amount=1000,
        status="OPEN",
        tenant_id=tenant_id,
    )

    db_session.add(receivable)


    payment = Payment(
        payment_number="REC-FULL-001",
        amount=1000,
        payment_method="TEST",
        status="COMPLETED",
        invoice_id=invoice.id,
        tenant_id=tenant_id,
    )

    db_session.add(payment)

    db_session.commit()


    receivable.paid_amount += 1000
    receivable.balance_amount = 0
    receivable.status = "PAID"

    db_session.commit()


    assert receivable.paid_amount == 1000
    assert receivable.balance_amount == 0
    assert receivable.status == "PAID"
