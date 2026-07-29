from sqlalchemy.orm import Session

from src.models.saas_core import (
    Receivable,
    CustomerCreditWallet,
)

from src.domains.accounting.services.journal_service import (
    create_customer_payment_journal,
)


def allocate_completed_payment(
    db: Session,
    payment,
    tenant_id: str,
):
    """
    Central Payment Allocation Engine

    Payment Completed
        |
        +--> Accounting Journal
        |
        +--> Receivable Allocation
        |
        +--> Customer Credit Wallet
    """

    invoice = payment.invoice

    if not invoice:
        raise Exception("INVOICE_NOT_FOUND")


    order = invoice.order

    if not order or not order.customer_id:
        raise Exception("CUSTOMER_NOT_FOUND")


    # ==========================
    # ACCOUNTING
    # ==========================

    create_customer_payment_journal(
        db=db,
        tenant_id=tenant_id,
        payment_id=payment.id,
        payment_amount=payment.amount,
    )


    # ==========================
    # RECEIVABLE
    # ==========================

    receivable = (
        db.query(Receivable)
        .filter(
            Receivable.invoice_id == invoice.id,
            Receivable.tenant_id == tenant_id,
        )
        .first()
    )


    if not receivable:

        receivable = Receivable(
            customer_id=order.customer_id,
            invoice_id=invoice.id,
            total_amount=invoice.amount,
            paid_amount=0,
            balance_amount=invoice.amount,
            status="OPEN",
            tenant_id=tenant_id,
        )

        db.add(receivable)
        db.flush()


    remaining_amount = (
        receivable.total_amount -
        receivable.paid_amount
    )


    applied_amount = min(
        payment.amount,
        remaining_amount
    )


    extra_credit = (
        payment.amount -
        applied_amount
    )


    receivable.paid_amount += applied_amount

    receivable.balance_amount = (
        receivable.total_amount -
        receivable.paid_amount
    )


    if receivable.balance_amount <= 0:

        receivable.balance_amount = 0
        receivable.status = "PAID"

    else:

        receivable.status = "PARTIAL"


    # ==========================
    # CUSTOMER CREDIT
    # ==========================

    if extra_credit > 0:

        wallet = (
            db.query(CustomerCreditWallet)
            .filter(
                CustomerCreditWallet.customer_id == order.customer_id,
                CustomerCreditWallet.tenant_id == tenant_id,
            )
            .first()
        )


        if not wallet:

            wallet = CustomerCreditWallet(
                customer_id=order.customer_id,
                credit_amount=0,
                tenant_id=tenant_id,
            )

            db.add(wallet)
            db.flush()


        wallet.credit_amount += extra_credit


    db.flush()

    return receivable
