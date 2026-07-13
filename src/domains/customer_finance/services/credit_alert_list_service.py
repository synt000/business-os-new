from sqlalchemy.orm import Session
from src.models.saas_core import CustomerCreditAlert

def get_credit_alerts(db: Session, tenant_id: str):
    alerts = (
        db.query(CustomerCreditAlert)
        .filter(CustomerCreditAlert.tenant_id == tenant_id)
        .order_by(CustomerCreditAlert.created_at.desc())
        .all()
    )

    return {
        "total_alerts": len(alerts),
        "alerts": [
            {
                "id": a.id,
                "customer_id": a.customer_id,
                "severity": a.severity,
                "status": a.status,
                "message": a.message
            }
            for a in alerts
        ]
    }
