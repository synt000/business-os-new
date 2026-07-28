from sqlalchemy import func
from sqlalchemy.orm import Session

from src.models.saas_core import (
    Payment,
    Invoice,
    Receivable,
    CustomerCreditWallet,
)

from src.domains.accounting.models import AccountLedger

from src.domains.accounting.services.journal_service import (
    create_customer_payment_journal,
)


def create_payment(
    db: Session,
    tenant_id: str,
    data,
):

    # ==============================
    # DUPLICATE PAYMENT CHECK
    # ==============================

    existing_payment = (
        db.query(Payment)
        .filter(
            Payment.payment_number == data.payment_number,
            Payment.tenant_id == tenant_id,
        )
        .first()
    )

    if existing_payment:
        raise Exception("DUPLICATE_PAYMENT_NUMBER")


    # ==============================
    # FIND INVOICE
    # ==============================

    invoice = (
        db.query(Invoice)
        .filter(
            Invoice.id == data.invoice_id,
            Invoice.tenant_id == tenant_id,
        )
        .first()
    )

    if not invoice:
        raise Exception("INVOICE_NOT_FOUND")


    # ==============================
    # OVER PAYMENT PROTECTION
    # ==============================

    from sqlalchemy import func

    paid_total = (
        db.query(func.sum(Payment.amount))
        .filter(
            Payment.invoice_id == invoice.id,
            Payment.status == "COMPLETED"
        )
        .scalar()
        or 0
    )

    remaining = invoice.amount - paid_total

    if data.amount > remaining:
        raise Exception("PAYMENT_EXCEEDS_BALANCE")


    # ==============================
    # CREATE PAYMENT
    # ==============================

    payment = Payment(
        payment_number=data.payment_number,
        amount=data.amount,
        payment_method=data.payment_method,
        status="COMPLETED",
        invoice_id=invoice.id,
        tenant_id=tenant_id,
    )

    db.add(payment)
    db.flush()


    create_customer_payment_journal(
        db=db,
        tenant_id=tenant_id,
        payment_id=payment.id,
        payment_amount=data.amount,
    )


    order = invoice.order

    if not order or not order.customer_id:
        raise Exception("CUSTOMER_NOT_FOUND")


    # ==============================
    # RECEIVABLE UPDATE
    # ==============================

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


    # ==============================
    # PAYMENT ALLOCATION ENGINE
    # ==============================

    remaining_amount = (
        receivable.total_amount -
        receivable.paid_amount
    )

    applied_amount = min(
        data.amount,
        remaining_amount
    )

    extra_credit = (
        data.amount -
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
        invoice.status = "PAID"
    else:
        receivable.status = "PARTIAL"
        invoice.status = "PARTIAL"




    # ==============================
    # CUSTOMER CREDIT WALLET
    # ==============================

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


    # ==============================
    # ACCOUNT LEDGER
    # ==============================

    # ==============================
    # LEDGER DUPLICATE PROTECTION
    # ==============================

    existing_ledger = (
        db.query(AccountLedger)
        .filter(
            AccountLedger.reference_id == data.payment_number,
            AccountLedger.account_head == "SALES_PAYMENT",
            AccountLedger.tenant_id == tenant_id,
        )
        .first()
    )

    ledger = None

    if not existing_ledger:
        ledger = AccountLedger(
            entry_type="INCOME",
            account_head="SALES_PAYMENT",
            amount=data.amount,
            reference_id=data.payment_number,
            description=f"Payment received {data.payment_number}",
            tenant_id=tenant_id,
        )


    db.add(payment)
    if ledger:
        db.add(ledger)

    db.commit()
    db.refresh(payment)

    return payment



def get_payments(
    db: Session,
    tenant_id: str,
):

    payments = (
        db.query(Payment)
        .filter(
            Payment.tenant_id == tenant_id
        )
        .order_by(
            Payment.created_at.desc()
        )
        .all()
    )

    result = []

    for p in payments:

        invoice = (
            db.query(Invoice)
            .filter(
                Invoice.id == p.invoice_id,
                Invoice.tenant_id == tenant_id
            )
            .first()
        )

        customer_name = ""

        if invoice and invoice.order:
            customer_name = invoice.order.customer_name or ""

        remaining = 0

        if invoice:

            paid = (
                db.query(func.sum(Payment.amount))
                .filter(
                    Payment.invoice_id == invoice.id,
                    Payment.status == "COMPLETED"
                )
                .scalar()
                or 0
            )

            remaining = invoice.amount - paid

        result.append({

            "payment_number": p.payment_number,

            "invoice_number":
                invoice.invoice_number
                if invoice else "",

            "customer_name":
                customer_name,

            "amount": p.amount,

            "payment_method":
                p.payment_method,

            "status":
                p.status,

            "remaining_balance":
                remaining,

            "created_at":
                p.created_at

        })

    return result

