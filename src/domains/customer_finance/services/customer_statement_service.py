from sqlalchemy.orm import Session

from src.models.saas_core import (
    Customer,
    Invoice,
    Payment,
    CustomerCreditWallet,
)


def get_customer_statement(
    db: Session,
    tenant_id: str,
    customer_id: str
):

    customer = (
        db.query(Customer)
        .filter(
            Customer.id == customer_id,
            Customer.tenant_id == tenant_id
        )
        .first()
    )

    if not customer:
        raise Exception("CUSTOMER_NOT_FOUND")


    invoices = (
        db.query(Invoice)
        .join(Invoice.order)
        .filter(
            Invoice.tenant_id == tenant_id,
            Invoice.order.has(
                customer_id=customer_id
            )
        )
        .all()
    )


    payments = (
        db.query(Payment)
        .join(Payment.invoice)
        .join(Invoice.order)
        .filter(
            Payment.tenant_id == tenant_id,
            Invoice.order.has(
                customer_id=customer_id
            )
        )
        .all()
    )


    transactions = []


    total_sales = 0
    total_paid = 0


    for invoice in invoices:
        total_sales += invoice.amount

        transactions.append({
            "type": "INVOICE",
            "number": invoice.invoice_number,
            "amount": invoice.amount,
            "status": invoice.status,
            "date": invoice.created_at
        })


    for payment in payments:
        total_paid += payment.amount

        transactions.append({
            "type": "PAYMENT",
            "number": payment.payment_number,
            "amount": payment.amount,
            "method": payment.payment_method,
            "date": payment.created_at
        })


    wallet = (
        db.query(CustomerCreditWallet)
        .filter(
            CustomerCreditWallet.customer_id == customer_id,
            CustomerCreditWallet.tenant_id == tenant_id
        )
        .first()
    )

    customer_credit = wallet.credit_amount if wallet else 0

    return {
        "customer_id": customer.id,
        "customer_name": customer.customer_name,
        "transactions": transactions,
        "summary": {
            "total_sales": total_sales,
            "total_paid": total_paid,
            "balance": max(total_sales - total_paid, 0),
            "customer_credit": customer_credit
        }
    }
