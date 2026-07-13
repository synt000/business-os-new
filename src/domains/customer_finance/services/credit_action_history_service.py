from sqlalchemy.orm import Session

from src.models.saas_core import CustomerCreditActionHistory


def get_credit_actions(
    db: Session,
    tenant_id: str,
    customer_id: str | None = None
):
    query = (
        db.query(CustomerCreditActionHistory)
        .filter(
            CustomerCreditActionHistory.tenant_id == tenant_id
        )
    )

    if customer_id:
        query = query.filter(
            CustomerCreditActionHistory.customer_id == customer_id
        )

    actions = (
        query
        .order_by(
            CustomerCreditActionHistory.created_at.desc()
        )
        .all()
    )

    return {
        "total_actions": len(actions),
        "actions": [
            {
                "id": a.id,
                "customer_id": a.customer_id,
                "action": a.action,
                "old_limit": a.old_limit,
                "new_limit": a.new_limit,
                "reason": a.reason,
                "credit_score": a.credit_score,
                "behavior_score": a.behavior_score
            }
            for a in actions
        ]
    }
