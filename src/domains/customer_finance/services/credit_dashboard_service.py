from sqlalchemy.orm import Session
from sqlalchemy import func

from src.models.saas_core import CustomerCreditRiskHistory


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

    aaa_count = (
        db.query(func.count(CustomerCreditRiskHistory.id))
        .filter(
            CustomerCreditRiskHistory.tenant_id == tenant_id,
            CustomerCreditRiskHistory.risk_level == "AAA"
        )
        .scalar()
    ) or 0


    a_count = (
        db.query(func.count(CustomerCreditRiskHistory.id))
        .filter(
            CustomerCreditRiskHistory.tenant_id == tenant_id,
            CustomerCreditRiskHistory.risk_level == "A"
        )
        .scalar()
    ) or 0


    b_count = (
        db.query(func.count(CustomerCreditRiskHistory.id))
        .filter(
            CustomerCreditRiskHistory.tenant_id == tenant_id,
            CustomerCreditRiskHistory.risk_level == "B"
        )
        .scalar()
    ) or 0

    c_count = (
        db.query(func.count(CustomerCreditRiskHistory.id))
        .filter(
            CustomerCreditRiskHistory.tenant_id == tenant_id,
            CustomerCreditRiskHistory.risk_level == "C"
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

    return {
        "total_customers": total_customers,
        "average_credit_score": round(average_score, 2),
        "risk_distribution": {
            "AAA": aaa_count,
            "A": a_count,
            "B": b_count,
            "C": c_count
        }
    }
