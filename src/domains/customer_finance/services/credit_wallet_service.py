from sqlalchemy.orm import Session

from src.models.saas_core import (
    CustomerCreditWallet,
    CustomerCreditTransaction,
    Invoice,
    Payment,
    Receivable,
    AccountLedger,
)


def get_credit_wallet(
    db: Session,
    tenant_id: str,
    customer_id: str
):
    wallet = (
        db.query(CustomerCreditWallet)
        .filter(
            CustomerCreditWallet.customer_id == customer_id,
            CustomerCreditWallet.tenant_id == tenant_id
        )
        .first()
    )

    if not wallet:
        return {
            "customer_id": customer_id,
            "credit_balance": 0
        }

    return {
        "customer_id": customer_id,
        "credit_balance": wallet.credit_amount
    }


def use_credit(
    db: Session,
    tenant_id: str,
    customer_id: str,
    amount: float
):
    wallet = (
        db.query(CustomerCreditWallet)
        .filter(
            CustomerCreditWallet.customer_id == customer_id,
            CustomerCreditWallet.tenant_id == tenant_id
        )
        .first()
    )

    if not wallet:
        raise Exception("WALLET_NOT_FOUND")

    if wallet.credit_amount < amount:
        raise Exception("INSUFFICIENT_CREDIT")

    wallet.credit_amount -= amount

    db.commit()
    db.refresh(wallet)

    return {
        "customer_id": customer_id,
        "used_credit": amount,
        "remaining_credit": wallet.credit_amount
    }




def use_credit_for_invoice(
    db: Session,
    tenant_id: str,
    customer_id: str,
    invoice_id: str,
    amount: float
):
    # ==============================
    # FIND WALLET
    # ==============================

    wallet = (
        db.query(CustomerCreditWallet)
        .filter(
            CustomerCreditWallet.customer_id == customer_id,
            CustomerCreditWallet.tenant_id == tenant_id
        )
        .first()
    )

    if not wallet:
        raise Exception("WALLET_NOT_FOUND")

    if wallet.credit_amount < amount:
        raise Exception("INSUFFICIENT_CREDIT")

    # ==============================
    # FIND INVOICE
    # ==============================

    invoice = (
        db.query(Invoice)
        .filter(
            Invoice.id == invoice_id,
            Invoice.tenant_id == tenant_id
        )
        .first()
    )

    if not invoice:
        raise Exception("INVOICE_NOT_FOUND")


    # ==============================
    # APPLY CREDIT
    # ==============================

    wallet.credit_amount -= amount

    if wallet.credit_amount < 0:
        wallet.credit_amount = 0


    # ==============================
    # UPDATE INVOICE
    # ==============================

    if invoice.status != "PAID":
        invoice.status = "PAID"


    # ==============================
    # ACCOUNT LEDGER
    # ==============================

    ledger = AccountLedger(
        entry_type="EXPENSE",
        account_head="CUSTOMER_CREDIT_USED",
        amount=amount,
        reference_id=invoice_id,
        description=f"Customer credit used for invoice {invoice_id}",
        tenant_id=tenant_id,
    )

    db.add(ledger)

    credit_tx = CustomerCreditTransaction(
        customer_id=customer_id,
        transaction_type="USE",
        amount=amount,
        invoice_id=invoice_id,
        tenant_id=tenant_id,
        notes=f"Credit used for invoice {invoice_id}"
    )

    db.add(credit_tx)


    db.commit()

    db.refresh(wallet)
    db.refresh(invoice)


    return {
        "customer_id": customer_id,
        "invoice_id": invoice_id,
        "used_credit": amount,
        "remaining_credit": wallet.credit_amount,
        "invoice_status": invoice.status
    }


def get_credit_history(
    db: Session,
    tenant_id: str,
    customer_id: str
):
    rows = (
        db.query(CustomerCreditTransaction)
        .filter(
            CustomerCreditTransaction.customer_id == customer_id,
            CustomerCreditTransaction.tenant_id == tenant_id
        )
        .order_by(CustomerCreditTransaction.created_at.desc())
        .all()
    )

    return [
        {
            "transaction_type": row.transaction_type,
            "amount": row.amount,
            "invoice_id": row.invoice_id,
            "payment_id": row.payment_id,
            "notes": row.notes,
            "created_at": row.created_at,
        }
        for row in rows
    ]


def topup_credit(
    db: Session,
    tenant_id: str,
    customer_id: str,
    amount: float,
    notes: str = "Manual credit top-up"
):
    wallet = (
        db.query(CustomerCreditWallet)
        .filter(
            CustomerCreditWallet.customer_id == customer_id,
            CustomerCreditWallet.tenant_id == tenant_id
        )
        .first()
    )

    if not wallet:
        raise Exception("WALLET_NOT_FOUND")

    new_balance = wallet.credit_amount + amount

    if wallet.credit_limit > 0:
        wallet.credit_amount = min(new_balance, wallet.credit_limit)
    else:
        wallet.credit_amount = new_balance

    ledger = AccountLedger(
        entry_type="INCOME",
        account_head="CUSTOMER_CREDIT_TOPUP",
        amount=amount,
        reference_id=customer_id,
        description=notes,
        tenant_id=tenant_id,
    )
    db.add(ledger)

    credit_tx = CustomerCreditTransaction(
        customer_id=customer_id,
        transaction_type="TOPUP",
        amount=amount,
        tenant_id=tenant_id,
        notes=notes
    )
    db.add(credit_tx)

    db.commit()

    db.refresh(wallet)

    return {
        "customer_id": customer_id,
        "topup_amount": amount,
        "credit_balance": wallet.credit_amount
    }


def refund_credit(
    db: Session,
    tenant_id: str,
    customer_id: str,
    amount: float,
    invoice_id: str = None,
    notes: str = "Credit refund"
):
    wallet = (
        db.query(CustomerCreditWallet)
        .filter(
            CustomerCreditWallet.customer_id == customer_id,
            CustomerCreditWallet.tenant_id == tenant_id
        )
        .first()
    )

    if not wallet:
        raise Exception("WALLET_NOT_FOUND")

    new_balance = wallet.credit_amount + amount

    if wallet.credit_limit > 0:
        wallet.credit_amount = min(new_balance, wallet.credit_limit)
    else:
        wallet.credit_amount = new_balance

    ledger = AccountLedger(
        entry_type="EXPENSE",
        account_head="CUSTOMER_CREDIT_REFUND",
        amount=amount,
        reference_id=invoice_id or customer_id,
        description=notes,
        tenant_id=tenant_id,
    )
    db.add(ledger)

    credit_tx = CustomerCreditTransaction(
        customer_id=customer_id,
        transaction_type="REFUND",
        amount=amount,
        invoice_id=invoice_id,
        tenant_id=tenant_id,
        notes=notes
    )
    db.add(credit_tx)

    db.commit()
    db.refresh(wallet)

    return {
        "customer_id": customer_id,
        "refund_amount": amount,
        "credit_balance": wallet.credit_amount
    }


def update_credit_limit(
    db: Session,
    tenant_id: str,
    customer_id: str,
    credit_limit: float
):
    wallet = (
        db.query(CustomerCreditWallet)
        .filter(
            CustomerCreditWallet.customer_id == customer_id,
            CustomerCreditWallet.tenant_id == tenant_id
        )
        .first()
    )

    if not wallet:
        raise Exception("WALLET_NOT_FOUND")

    wallet.credit_limit = credit_limit

    db.commit()
    db.refresh(wallet)

    return {
        "customer_id": customer_id,
        "credit_limit": wallet.credit_limit,
        "credit_balance": wallet.credit_amount
    }
