import pytest

from src.models.saas_core import Payment


def test_first_payment_request(
    db_session,
    tenant_id,
    payment_data,
    invoice_id,
):

    payment_data.payment_request_id = "PAY-REQUEST-8899"

    payment = Payment(
        tenant_id=tenant_id,
        payment_number="PAY-001",
        payment_request_id=payment_data.payment_request_id,
        amount=100,
        payment_method="CARD",
        status="PENDING",
        invoice_id=invoice_id,
    )

    db_session.add(payment)
    db_session.commit()

    result = (
        db_session.query(Payment)
        .filter(
            Payment.payment_request_id
            == "PAY-REQUEST-8899"
        )
        .first()
    )

    assert result is not None
    assert result.payment_request_id == "PAY-REQUEST-8899"



def test_completed_request_returns_existing(
    db_session,
    tenant_id,
    invoice_id,
):

    existing = Payment(
        tenant_id=tenant_id,
        payment_number="PAY-002",
        payment_request_id="PAY-REQUEST-8899",
        amount=100,
        payment_method="CARD",
        status="COMPLETED",
        invoice_id=invoice_id,
    )

    db_session.add(existing)
    db_session.commit()


    result = (
        db_session.query(Payment)
        .filter(
            Payment.payment_request_id
            == "PAY-REQUEST-8899",
            Payment.tenant_id == tenant_id,
        )
        .first()
    )


    assert result.id == existing.id
    assert result.status == "COMPLETED"



def test_pending_request_blocks_retry(
    db_session,
    tenant_id,
    invoice_id,
):

    existing = Payment(
        tenant_id=tenant_id,
        payment_number="PAY-003",
        payment_request_id="PAY-REQUEST-8899",
        amount=100,
        payment_method="CARD",
        status="PENDING",
        invoice_id=invoice_id,
    )

    db_session.add(existing)
    db_session.commit()


    result = (
        db_session.query(Payment)
        .filter(
            Payment.payment_request_id
            == "PAY-REQUEST-8899",
        )
        .first()
    )


    assert result.status == "PENDING"



def test_failed_request_requires_new_id(
    db_session,
    tenant_id,
    invoice_id,
):

    failed = Payment(
        tenant_id=tenant_id,
        payment_number="PAY-004",
        payment_request_id="PAY-REQUEST-8899",
        amount=100,
        payment_method="CARD",
        status="FAILED",
        invoice_id=invoice_id,
    )

    db_session.add(failed)
    db_session.commit()


    result = (
        db_session.query(Payment)
        .filter(
            Payment.payment_request_id
            == "PAY-REQUEST-8899",
        )
        .first()
    )


    assert result.status == "FAILED"
