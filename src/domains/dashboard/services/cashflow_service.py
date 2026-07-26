from sqlalchemy import func

from src.models.saas_core import Invoice, Payment


def get_cashflow_dashboard(db, tenant_id):

    total_revenue = (
        db.query(func.sum(Invoice.amount))
        .filter(
            Invoice.tenant_id == tenant_id,
            Invoice.invoice_number.like("INV-%"),
        )
        .scalar()
        or 0
    )


    total_collected = (
        db.query(func.sum(Payment.amount))
        .filter(
            Payment.tenant_id == tenant_id,
            Payment.status == "COMPLETED"
        )
        .scalar()
        or 0
    )


    pending_receivable = (
        total_revenue - total_collected
    )


    paid = (
        db.query(func.count(Invoice.id))
        .filter(
            Invoice.tenant_id == tenant_id,
            Invoice.invoice_number.like("INV-%"),
            Invoice.status == "PAID"
        )
        .scalar()
        or 0
    )


    partial = (
        db.query(func.count(Invoice.id))
        .filter(
            Invoice.tenant_id == tenant_id,
            Invoice.invoice_number.like("INV-%"),
            Invoice.status == "PARTIAL"
        )
        .scalar()
        or 0
    )


    unpaid = (
        db.query(func.count(Invoice.id))
        .filter(
            Invoice.tenant_id == tenant_id,
            Invoice.invoice_number.like("INV-%"),
            Invoice.status == "UNPAID"
        )
        .scalar()
        or 0
    )


    methods = {}

    rows = (
        db.query(
            Payment.payment_method,
            func.sum(Payment.amount)
        )
        .filter(
            Payment.tenant_id == tenant_id,
            Payment.status == "COMPLETED"
        )
        .group_by(
            Payment.payment_method
        )
        .all()
    )


    for method, amount in rows:
        methods[method] = float(amount)


    return {
        "total_revenue": float(total_revenue),
        "total_collected": float(total_collected),
        "pending_receivable": float(pending_receivable),
        "invoice_summary": {
            "paid": paid,
            "partial": partial,
            "unpaid": unpaid
        },
        "payment_methods": methods
    }
