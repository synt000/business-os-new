from sqlalchemy import func
from sqlalchemy.orm import Session

from src.models.saas_core import (
    Payment,
    Invoice,
    Receivable,
    CustomerCreditWallet,
)

from src.domains.accounting.models import AccountLedger
from src.domains.audit.service import AuditService

from src.domains.accounting.services.journal_service import (
    create_customer_payment_journal,
)

from src.domains.accounting.services.payment_account_resolver import (
    resolve_payment_account,
)



def sync_invoice_payment_state(
    db: Session,
    invoice: Invoice,
    tenant_id: str,
):
    """
    Sync Invoice and Order status after payment.
    """

    paid_total = (
        db.query(func.sum(Payment.amount))
        .filter(
            Payment.invoice_id == invoice.id,
            Payment.status == "COMPLETED",
            Payment.tenant_id == tenant_id,
        )
        .scalar()
        or 0
    )


    if paid_total >= invoice.amount:
        invoice.status = "PAID"

        if invoice.order:
            invoice.order.order_status = "PAID"

    elif paid_total > 0:
        invoice.status = "PARTIAL"

    else:
        invoice.status = "UNPAID"



def create_payment(
    db: Session,
    tenant_id: str,
    data,
):

    # ==============================
    # IDEMPOTENCY REQUEST CHECK
    # ==============================

    if getattr(data, "payment_request_id", None):

        existing_request = (
            db.query(Payment)
            .filter(
                Payment.payment_request_id == data.payment_request_id,
                Payment.tenant_id == tenant_id,
            )
            .first()
        )

        if existing_request:

            # ==============================
            # IDEMPOTENCY STATE HANDLING
            # ==============================

            if existing_request.status == "COMPLETED":
                return existing_request


            if existing_request.status == "PENDING":
                raise Exception(
                    "PAYMENT_REQUEST_ALREADY_PROCESSING"
                )


            if existing_request.status == "FAILED":
                raise Exception(
                    "PAYMENT_REQUEST_FAILED_RETRY_WITH_NEW_ID"
                )


            return existing_request


    # ==============================
    # DUPLICATE PAYMENT NUMBER CHECK
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


    payment_account = resolve_payment_account(
        db,
        tenant_id,
        data.payment_method,
    )

    create_customer_payment_journal(
        db=db,
        tenant_id=tenant_id,
        payment_id=payment.id,
        payment_amount=data.amount,
        payment_account=payment_account,
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


    sync_invoice_payment_state(
        db,
        invoice,
        tenant_id,
    )




    AuditService.create_audit_log(
        db=db,
        tenant_id=tenant_id,
        action="PAYMENT_COMPLETED",
        table_name="payments",
        record_id=str(payment.id),
        changes="{}",
    )


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

