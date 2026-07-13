from sqlalchemy.orm import Session

from src.domains.customer_finance.services.credit_risk_service import (
    calculate_customer_credit_score
)

from src.domains.customer_finance.services.credit_behavior_service import (
    analyze_credit_behavior
)

from src.models.saas_core import CustomerCreditWallet


def make_credit_decision(
    db: Session,
    tenant_id: str,
    customer_id: str
):

    risk = calculate_customer_credit_score(
        db=db,
        tenant_id=tenant_id,
        customer_id=customer_id
    )

    behavior = analyze_credit_behavior(
        db=db,
        tenant_id=tenant_id,
        customer_id=customer_id
    )

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


    current_limit = wallet.credit_limit

    decision = "MAINTAIN_LIMIT"
    new_limit = current_limit
    reason = "NORMAL_BEHAVIOR"


    if (
        risk["credit_score"] >= 85
        and behavior["behavior_score"] >= 80
    ):
        decision = "INCREASE_LIMIT"
        new_limit = current_limit * 1.25
        reason = "GOOD_PAYMENT_BEHAVIOR"


    elif (
        risk["credit_score"] < 50
        or behavior["behavior_score"] < 50
    ):
        decision = "REDUCE_LIMIT"
        new_limit = current_limit * 0.75
        reason = "HIGH_CREDIT_RISK"


    return {
        "customer_id": customer_id,
        "decision": decision,
        "current_limit": current_limit,
        "recommended_limit": round(new_limit, 2),
        "reason": reason,
        "credit_score": risk["credit_score"],
        "behavior_score": behavior["behavior_score"]
    }
