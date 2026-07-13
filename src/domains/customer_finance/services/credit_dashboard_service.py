from sqlalchemy.orm import Session
from sqlalchemy import func

from src.models.saas_core import (
    CustomerCreditRiskHistory,
    CustomerCreditWallet,
    CustomerCreditActionHistory,
    CustomerCreditAlert
)


def get_credit_risk_dashboard(
    db: Session,
    tenant_id: str
):

    total_customers = (
        db.query(func.count(CustomerCreditRiskHistory.id))
        .filter(
            CustomerCreditRiskHistory.tenant_id == tenant_id
        )
        .scalar()
    ) or 0


    average_score = (
        db.query(func.avg(CustomerCreditRiskHistory.credit_score))
        .filter(
            CustomerCreditRiskHistory.tenant_id == tenant_id
        )
        .scalar()
    ) or 0


    risk_distribution = {}

    for level in ["AAA", "A", "B", "C"]:
        risk_distribution[level] = (
           
        db.query(func.count(CustomerCreditRiskHistory.id))
        .filter(
            CustomerCreditRiskHistory.tenant_id == tenant_id,
            CustomerCreditRiskHistory.risk_level == level
        )
        .scalar()
    ) or 0


    total_credit_limit = (
        db.query(func.sum(CustomerCreditWallet.credit_limit))
        .filter(
            CustomerCreditWallet.tenant_id == tenant_id
        )
        .scalar()
    ) or 0


    total_credit_balance = (
        db.query(func.sum(CustomerCreditWallet.credit_amount))
        .filter(
            CustomerCreditWallet.tenant_id == tenant_id
        )
        .scalar()
    ) or 0


    action_summary = {}

    for action in [
        "LIMIT_INCREASED",
        "LIMIT_REDUCED",
        "LIMIT_MAINTAINED"
    ]:
        action_summary[action] = (
            db.query(func.count(CustomerCreditActionHistory.id))
            .filter(
                CustomerCreditActionHistory.tenant_id == tenant_id,
                CustomerCreditActionHistory.action == action
            )
            .scalar()
        ) or 0

    
    alert_summary = {
        "total": db.query(func.count(CustomerCreditAlert.id))
        .filter(CustomerCreditAlert.tenant_id == tenant_id)
        .scalar() or 0,
        "open": db.query(func.count(CustomerCreditAlert.id))
        .filter(
            CustomerCreditAlert.tenant_id == tenant_id,
            CustomerCreditAlert.status == "OPEN"
        )
        .scalar() or 0,
        "resolved": db.query(func.count(CustomerCreditAlert.id))
        .filter(
            CustomerCreditAlert.tenant_id == tenant_id,
            CustomerCreditAlert.status == "RESOLVED"
        )
        .scalar() or 0
    }


    return {
        "total_customers": total_customers,
        "average_credit_score": round(average_score, 2),
        "risk_distribution": risk_distribution,
        "credit_exposure": {
            "total_credit_limit": round(total_credit_limit, 2),
            "total_credit_balance": round(total_credit_balance, 2)
        },
        "action_summary": action_summary,
        "alert_summary": alert_summary
    }
