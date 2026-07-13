from sqlalchemy.orm import Session

from src.models.saas_core import CustomerCreditActionHistory


def get_customer_credit_history(
    db: Session,
    tenant_id: str,
    customer_id: str
):

    histories = (
        db.query(CustomerCreditActionHistory)
        .filter(
            CustomerCreditActionHistory.customer_id == customer_id,
            CustomerCreditActionHistory.tenant_id == tenant_id
        )
        .order_by(
            CustomerCreditActionHistory.created_at.desc()
        )
        .all()
    )

    return {
        "customer_id": customer_id,
        "total_actions": len(histories),
        "history": [
            {
                "action": item.action,
                "old_limit": item.old_limit,
                "new_limit": item.new_limit,
                "reason": item.reason,
                "credit_score": item.credit_score,
                "behavior_score": item.behavior_score,
                "created_at": item.created_at.isoformat() if item.created_at else None
            }
            for item in histories
        ]
    }
