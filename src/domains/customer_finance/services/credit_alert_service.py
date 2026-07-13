from sqlalchemy.orm import Session

from src.models.saas_core import CustomerCreditAlert


def create_credit_alert(
    db: Session,
    tenant_id: str,
    customer_id: str,
    alert_type: str,
    severity: str,
    message: str
):

    alert = CustomerCreditAlert(
        tenant_id=tenant_id,
        customer_id=customer_id,
        alert_type=alert_type,
        severity=severity,
        message=message
    )

    db.add(alert)
    db.commit()
    db.refresh(alert)

    return {
        "alert_id": alert.id,
        "status": alert.status,
        "severity": alert.severity
    }
