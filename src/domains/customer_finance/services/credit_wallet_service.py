from sqlalchemy.orm import Session

from src.models.saas_core import CustomerCreditWallet


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
