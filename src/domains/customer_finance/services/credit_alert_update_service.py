from sqlalchemy.orm import Session
from src.models.saas_core import CustomerCreditAlert

def resolve_credit_alert(db: Session, tenant_id: str, alert_id: str):
    alert = (
        db.query(CustomerCreditAlert)
        .filter(
            CustomerCreditAlert.id == alert_id,
            CustomerCreditAlert.tenant_id == tenant_id
        )
        .first()
    )

    if not alert:
        return {"error":"ALERT_NOT_FOUND"}

    alert.status = "RESOLVED"
    db.commit()

    return {
        "alert_id": alert.id,
        "status": alert.status
    }
