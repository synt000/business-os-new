from sqlalchemy.orm import Session
from sqlalchemy import func

from src.models.saas_core import (
    CustomerCreditTransaction
)


def analyze_credit_behavior(
    db: Session,
    tenant_id: str,
    customer_id: str
):

    total_transactions = (
        db.query(func.count(CustomerCreditTransaction.id))
        .filter(
            CustomerCreditTransaction.customer_id == customer_id,
            CustomerCreditTransaction.tenant_id == tenant_id
        )
        .scalar()
    ) or 0


    total_paid = (
        db.query(func.sum(CustomerCreditTransaction.amount))
        .filter(
            CustomerCreditTransaction.customer_id == customer_id,
            CustomerCreditTransaction.tenant_id == tenant_id,
            CustomerCreditTransaction.transaction_type == "PAYMENT"
        )
        .scalar()
    ) or 0


    total_used = (
        db.query(func.sum(CustomerCreditTransaction.amount))
        .filter(
            CustomerCreditTransaction.customer_id == customer_id,
            CustomerCreditTransaction.tenant_id == tenant_id,
            CustomerCreditTransaction.transaction_type == "USE"
        )
        .scalar()
    ) or 0


    behavior_score = 50


    if total_transactions >= 5:
        behavior_score += 20


    if total_paid > 0:
        behavior_score += 20


    if total_used > total_paid:
        behavior_score -= 20


    behavior_score = max(
        min(behavior_score, 100),
        0
    )


    if behavior_score >= 80:
        recommendation = "CREDIT_INCREASE"

    elif behavior_score >= 50:
        recommendation = "MAINTAIN_LIMIT"

    else:
        recommendation = "CREDIT_REVIEW_REQUIRED"


    return {
        "customer_id": customer_id,
        "total_transactions": total_transactions,
        "total_paid": total_paid,
        "total_used": total_used,
        "behavior_score": behavior_score,
        "recommendation": recommendation
    }
