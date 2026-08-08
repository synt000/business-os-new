from src.domains.payment.services.payment_service import (
    sync_invoice_payment_state,
)
from src.models.saas_core import Invoice, Order, Payment


def test_full_payment_sets_order_to_paid_not_completed(
    db_session,
    tenant_id,
    invoice_id,
):
    invoice = (
        db_session.query(Invoice)
        .filter(
            Invoice.id == invoice_id,
            Invoice.tenant_id == tenant_id,
        )
        .first()
    )

    order = (
        db_session.query(Order)
        .filter(
            Order.id == invoice.order_id,
            Order.tenant_id == tenant_id,
        )
        .first()
    )

    order.order_status = "SHIPPED"

    payment = Payment(
        payment_number="ORDER-STATE-SYNC-001",
        amount=invoice.amount,
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
    assert order.order_status == "PAID"
    assert order.order_status != "COMPLETED"
