from datetime import datetime, timezone

from sqlalchemy.orm import Session
from sqlalchemy import func

from src.models.security_event import SecurityEvent


def get_security_overview(
    db: Session,
    tenant_id: str
):
    now = datetime.now(timezone.utc)

    today_start = now.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

    today_new_devices = (
        db.query(func.count(SecurityEvent.id))
        .filter(
            SecurityEvent.tenant_id == tenant_id,
            SecurityEvent.event_type == "NEW_DEVICE_LOGIN",
            SecurityEvent.created_at >= today_start
        )
        .scalar()
        or 0
    )

    medium_risk_logins = (
        db.query(func.count(SecurityEvent.id))
        .filter(
            SecurityEvent.tenant_id == tenant_id,
            SecurityEvent.risk_level == "MEDIUM",
            SecurityEvent.created_at >= today_start
        )
        .scalar()
        or 0
    )

    high_risk_logins = (
        db.query(func.count(SecurityEvent.id))
        .filter(
            SecurityEvent.tenant_id == tenant_id,
            SecurityEvent.risk_level == "HIGH",
            SecurityEvent.created_at >= today_start
        )
        .scalar()
        or 0
    )

    blocked_devices = (
        db.query(func.count(SecurityEvent.id))
        .filter(
            SecurityEvent.tenant_id == tenant_id,
            SecurityEvent.event_type == "DEVICE_BLOCKED",
            SecurityEvent.created_at >= today_start
        )
        .scalar()
        or 0
    )

    latest_events = (
        db.query(SecurityEvent)
        .filter(
            SecurityEvent.tenant_id == tenant_id
        )
        .order_by(
            SecurityEvent.created_at.desc()
        )
        .limit(10)
        .all()
    )

    return {
        "today_new_devices": today_new_devices,
        "medium_risk_logins": medium_risk_logins,
        "high_risk_logins": high_risk_logins,
        "blocked_devices": blocked_devices,
        "latest_events": [
            {
                "event": event.event_type,
                "risk": event.risk_level,
                "score": event.risk_score,
                "login_session_id": event.login_session_id,
                "device_session_id": event.device_session_id,
                "time": (
                    event.created_at.isoformat()
                    if event.created_at
                    else None
                ),
            }
            for event in latest_events
        ],
    }
