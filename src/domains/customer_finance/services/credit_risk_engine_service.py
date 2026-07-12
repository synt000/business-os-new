from sqlalchemy.orm import Session

from src.models.saas_core import (
    CustomerCreditWallet,
    CustomerCreditTransaction,
    CustomerCreditRiskHistory
)


def recalculate_customer_credit_risk(
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
        db.query(CustomerCreditTransaction)
        .filter(
            CustomerCreditTransaction.customer_id == customer_id,
            CustomerCreditTransaction.tenant_id == tenant_id
        )
        .count()
    )


    total_used_credit = (
        db.query(CustomerCreditTransaction)
        .filter(
            CustomerCreditTransaction.customer_id == customer_id,
            CustomerCreditTransaction.tenant_id == tenant_id,
            CustomerCreditTransaction.transaction_type == "USE"
        )
        .with_entities(
            CustomerCreditTransaction.amount
        )
        .all()
    )


    used_amount = sum(
        item[0] for item in total_used_credit
    )


    score = 50


    # Transaction history
    if total_transactions >= 5:
        score += 20


    # Active credit usage
    if used_amount > 0:
        score += 10


    # Remaining credit health
    if wallet.credit_limit > 0:
        utilization = (
            wallet.credit_amount /
            wallet.credit_limit
        )

        if utilization < 0.5:
            score += 20

        elif utilization > 0.9:
            score -= 20


    score = max(min(score, 100), 0)


    if score >= 90:
        risk_level = "AAA"

    elif score >= 75:
        risk_level = "A"

    elif score >= 50:
        risk_level = "B"

    else:
        risk_level = "C"



    history = CustomerCreditRiskHistory(
        customer_id=customer_id,
        credit_score=score,
        risk_level=risk_level,
        credit_balance=wallet.credit_amount,
        credit_limit=wallet.credit_limit,
        tenant_id=tenant_id
    )


    db.add(history)
    db.commit()
    db.refresh(history)


    return {
        "customer_id": customer_id,
        "credit_score": score,
        "risk_level": risk_level,
        "credit_balance": wallet.credit_amount,
        "credit_limit": wallet.credit_limit,
        "transactions": total_transactions
    }
