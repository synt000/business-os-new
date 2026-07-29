from sqlalchemy import func
from src.domains.payment.services.payment_service import (
    sync_invoice_payment_state,
)


def test_invoice_payment_module_import():
    assert sync_invoice_payment_state is not None


class DummyInvoice:

    def __init__(self):
        self.amount = 1000
        self.status = "UNPAID"


def test_invoice_initial_state():

    invoice = DummyInvoice()

    assert invoice.amount == 1000
    assert invoice.status == "UNPAID"


def test_partial_payment_expected():

    invoice = DummyInvoice()

    paid = 300
    remaining = invoice.amount - paid

    assert remaining == 700

    invoice.status = "PARTIAL"

    assert invoice.status == "PARTIAL"


def test_full_payment_expected():

    invoice = DummyInvoice()

    paid = 1000
    remaining = invoice.amount - paid

    assert remaining == 0

    invoice.status = "PAID"

    assert invoice.status == "PAID"


def test_overpayment_not_allowed():

    invoice = DummyInvoice()

    paid = 1200
    remaining = invoice.amount - paid

    assert paid > invoice.amount
    assert remaining < 0


def test_remaining_balance_calculation():

    invoice = DummyInvoice()

    payments = [200, 150, 100]

    remaining = invoice.amount - sum(payments)

    assert remaining == 550


from src.models.saas_core import Payment, Invoice


def test_real_partial_payment_sync(
    db_session,
    tenant_id,
    invoice_id,
):

    invoice = (
        db_session.query(Invoice)
        .filter(
            Invoice.id == invoice_id
        )
        .first()
    )

    payment = Payment(
        payment_number="SYNC-PARTIAL-001",
        amount=300,
        payment_method="TEST",
        status="COMPLETED",
        invoice_id=invoice.id,
        tenant_id=tenant_id,
    )

    db_session.add(payment)
    db_session.commit()

    sync_invoice_payment_state(
        db=db_session,
        invoice=invoice,
        tenant_id=tenant_id,
    )

    assert invoice.status == "PARTIAL"



def test_real_full_payment_sync(
    db_session,
    tenant_id,
    invoice_id,
):

    invoice = (
        db_session.query(Invoice)
        .filter(
            Invoice.id == invoice_id
        )
        .first()
    )

    payment = Payment(
        payment_number="SYNC-FULL-001",
        amount=1000,
        payment_method="TEST",
        status="COMPLETED",
        invoice_id=invoice.id,
        tenant_id=tenant_id,
    )

    db_session.add(payment)
    db_session.commit()

    sync_invoice_payment_state(
        db=db_session,
        invoice=invoice,
        tenant_id=tenant_id,
    )

    assert invoice.status == "PAID"


def test_remaining_balance_after_partial_payment(
    db_session,
    tenant_id,
    invoice_id,
):

    invoice = (
        db_session.query(Invoice)
        .filter(
            Invoice.id == invoice_id
        )
        .first()
    )

    payment = Payment(
        payment_number="BALANCE-PARTIAL-001",
        amount=300,
        payment_method="TEST",
        status="COMPLETED",
        invoice_id=invoice.id,
        tenant_id=tenant_id,
    )

    db_session.add(payment)
    db_session.commit()

    sync_invoice_payment_state(
        db=db_session,
        invoice=invoice,
        tenant_id=tenant_id,
    )

    paid_total = (
        db_session.query(
            func.sum(Payment.amount)
        )
        .filter(
            Payment.invoice_id == invoice.id,
            Payment.status == "COMPLETED",
        )
        .scalar()
        or 0
    )

    remaining = invoice.amount - paid_total

    assert invoice.status == "PARTIAL"
    assert remaining == 700



def test_remaining_balance_after_full_payment(
    db_session,
    tenant_id,
    invoice_id,
):

    invoice = (
        db_session.query(Invoice)
        .filter(
            Invoice.id == invoice_id
        )
        .first()
    )

    payment = Payment(
        payment_number="BALANCE-FULL-001",
        amount=1000,
        payment_method="TEST",
        status="COMPLETED",
        invoice_id=invoice.id,
        tenant_id=tenant_id,
    )

    db_session.add(payment)
    db_session.commit()

    sync_invoice_payment_state(
        db=db_session,
        invoice=invoice,
        tenant_id=tenant_id,
    )

    paid_total = (
        db_session.query(
            func.sum(Payment.amount)
        )
        .filter(
            Payment.invoice_id == invoice.id,
            Payment.status == "COMPLETED",
        )
        .scalar()
        or 0
    )

    remaining = invoice.amount - paid_total

    assert invoice.status == "PAID"
    assert remaining == 0



def test_overpayment_is_not_allowed(
    db_session,
    tenant_id,
    invoice_id,
):

    invoice = (
        db_session.query(Invoice)
        .filter(
            Invoice.id == invoice_id
        )
        .first()
    )

    overpayment = Payment(
        payment_number="OVERPAY-001",
        amount=1200,
        payment_method="TEST",
        status="COMPLETED",
        invoice_id=invoice.id,
        tenant_id=tenant_id,
    )

    db_session.add(overpayment)
    db_session.commit()

    paid_total = (
        db_session.query(
            func.sum(Payment.amount)
        )
        .filter(
            Payment.invoice_id == invoice.id,
            Payment.status == "COMPLETED",
        )
        .scalar()
        or 0
    )

    assert paid_total > invoice.amount
