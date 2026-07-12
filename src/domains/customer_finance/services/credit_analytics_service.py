from sqlalchemy.orm import Session
from sqlalchemy import func

from src.models.saas_core import CustomerCreditWallet


def get_credit_summary(
    db: Session,
    tenant_id: str
):
    result = (
        db.query(
            func.count(CustomerCreditWallet.id),
            func.sum(CustomerCreditWallet.credit_limit),
            func.sum(CustomerCreditWallet.credit_amount)
        )
        .filter(
            CustomerCreditWallet.tenant_id == tenant_id
        )
        .first()
    )

    total_customers = result[0] or 0
    total_credit_limit = result[1] or 0
    available_balance = result[2] or 0

    return {
        "total_customers": total_customers,
        "total_credit_limit": total_credit_limit,
        "total_available_balance": available_balance,
        "credit_utilization": max(
            total_credit_limit - available_balance,
            0
        )
    }
