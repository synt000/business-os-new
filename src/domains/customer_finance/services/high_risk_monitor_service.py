from sqlalchemy.orm import Session
from sqlalchemy import func

from src.models.saas_core import (
    CustomerCreditRiskHistory,
    CustomerCreditWallet
)


def get_high_risk_customers(
    db: Session,
    tenant_id: str
):

    latest_ids = (
        db.query(
            CustomerCreditRiskHistory.customer_id,
            func.max(CustomerCreditRiskHistory.calculated_at).label("latest")
        )
        .filter(
            CustomerCreditRiskHistory.tenant_id == tenant_id
        )
        .group_by(
            CustomerCreditRiskHistory.customer_id
        )
        .subquery()
    )


    risks = (
        db.query(CustomerCreditRiskHistory)
        .join(
            latest_ids,
            (CustomerCreditRiskHistory.customer_id == latest_ids.c.customer_id)
            &
            (CustomerCreditRiskHistory.calculated_at == latest_ids.c.latest)
        )
        .all()
    )


    high_risk = []


    for risk in risks:

        wallet = (
            db.query(CustomerCreditWallet)
            .filter(
                CustomerCreditWallet.customer_id == risk.customer_id,
                CustomerCreditWallet.tenant_id == tenant_id
            )
            .first()
        )


        if not wallet:
            continue


        if (
            risk.credit_score < 60
            or wallet.credit_amount > wallet.credit_limit * 0.8
        ):

            action = "CREDIT_REVIEW_REQUIRED"

            if risk.credit_score < 40:
                action = "LIMIT_REDUCTION_REQUIRED"


            high_risk.append(
                {
                    "customer_id": risk.customer_id,
                    "credit_score": risk.credit_score,
                    "risk_level": risk.risk_level,
                    "credit_limit": wallet.credit_limit,
                    "credit_amount": wallet.credit_amount,
                    "recommended_action": action
                }
            )


    return {
        "total_high_risk_customers": len(high_risk),
        "customers": high_risk
    }
