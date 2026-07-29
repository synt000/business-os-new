from sqlalchemy import func

from src.models.saas_core import Payment, Invoice, Receivable
from src.domains.payment.webhook.service import (
    handle_payment_completed_webhook,
)
from src.domains.accounting.models import AccountLedger


def test_payment_webhook_end_to_end(
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
        payment_number="E2E-PAY-001",
        amount=1000,
        payment_method="TEST",
        status="PENDING",
        invoice_id=invoice.id,
        tenant_id=tenant_id,
    )

    db_session.add(payment)
    db_session.commit()

    result = handle_payment_completed_webhook(
        db=db_session,
        tenant_id=tenant_id,
        payment_id=payment.id,
        event_id="evt_e2e_001",
        provider="stripe",
    )

    assert result["status"] == "completed"

    updated_payment = (
        db_session.query(Payment)
        .filter(
            Payment.id == payment.id
        )
        .first()
    )

    assert updated_payment.status == "COMPLETED"

    db_session.refresh(invoice)

    assert invoice.status == "PAID"


    # ==========================
    # RECEIVABLE ASSERTION
    # ==========================

    receivable = (
        db_session.query(Receivable)
        .filter(
            Receivable.invoice_id == invoice.id
        )
        .first()
    )

    assert receivable is not None
    assert receivable.status == "PAID"
    assert receivable.paid_amount == 1000


    # ==========================
    # LEDGER ASSERTION
    # ==========================

    ledger_entries = (
        db_session.query(AccountLedger)
        .filter(
            AccountLedger.reference_id == payment.id
        )
        .all()
    )

    assert len(ledger_entries) == 2

    heads = {
        entry.account_head
        for entry in ledger_entries
    }

    assert "CASH_ASSET" in heads
    assert "CUSTOMER_RECEIVABLE" in heads


def test_webhook_duplicate_blocked(
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
        payment_number="E2E-DUP-001",
        amount=500,
        payment_method="TEST",
        status="PENDING",
        invoice_id=invoice.id,
        tenant_id=tenant_id,
    )

    db_session.add(payment)
    db_session.commit()

    first = handle_payment_completed_webhook(
        db=db_session,
        tenant_id=tenant_id,
        payment_id=payment.id,
        event_id="evt_duplicate_e2e",
        provider="stripe",
    )

    second = handle_payment_completed_webhook(
        db=db_session,
        tenant_id=tenant_id,
        payment_id=payment.id,
        event_id="evt_duplicate_e2e",
        provider="stripe",
    )

    assert first["status"] == "completed"
    assert second["status"] == "duplicate"
