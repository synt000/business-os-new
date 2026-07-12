from sqlalchemy.orm import Session
from sqlalchemy import func

from src.models.saas_core import (
    CustomerCreditTransaction,
    CustomerCreditWallet,
    CustomerCreditRiskHistory
)


def calculate_customer_credit_score(
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
        raise Exception("WALLET_NOT_FOUND")


    total_transactions = (
        db.query(func.count(CustomerCreditTransaction.id))
        .filter(
            CustomerCreditTransaction.customer_id == customer_id,
            CustomerCreditTransaction.tenant_id == tenant_id
        )
        .scalar()
    ) or 0


    score = 50


    if total_transactions > 5:
        score += 20

    if wallet.credit_amount > 0:
        score += 20


    score = min(score, 100)


    if score >= 90:
        risk_level = "AAA"

    elif score >= 75:
        risk_level = "A"

    elif score >= 50:
        risk_level = "B"

    else:
        risk_level = "C"


    risk_history = CustomerCreditRiskHistory(
        customer_id=customer_id,
        credit_score=score,
        risk_level=risk_level,
        credit_balance=wallet.credit_amount,
        credit_limit=wallet.credit_limit,
        tenant_id=tenant_id
    )

    db.add(risk_history)
    db.commit()

    return {
        "customer_id": customer_id,
        "credit_score": score,
        "risk_level": risk_level,
        "current_credit_balance": wallet.credit_amount,
        "credit_limit": wallet.credit_limit
    }
