from fastapi import Request
import json
from sqlalchemy.orm import Session

from src.models.security_event import SecurityEvent


def get_client_ip(request: Request):
    """
    Extract client IP safely
    """

    if request.client:
        return request.client.host

    return "UNKNOWN"



def log_security_event(
    db: Session,
    *,
    event_type: str,
    user_id: str | None = None,
    tenant_id: str | None = None,
    request: Request | None = None,
    device_info: dict | str | None = None,
    login_session_id: str | None = None,
    device_session_id: str | None = None,
    risk_score: str | None = None,
    risk_level: str = "LOW",
    description: str | None = None,
    severity: str = "INFO",
):

    ip_address = None
    user_agent = None


    if request:

        ip_address = get_client_ip(request)

        user_agent = request.headers.get(
            "user-agent",
            "UNKNOWN"
        )


    if isinstance(device_info, dict):
        device_info = json.dumps(device_info)


    event = SecurityEvent(

        user_id=user_id,

        tenant_id=tenant_id,

        event_type=event_type,

        severity=severity,

        ip_address=ip_address,

        user_agent=user_agent,

        device_info=device_info,

        login_session_id=login_session_id,
        device_session_id=device_session_id,
        risk_score=risk_score,
        risk_level=risk_level,

        description=description,
    )


    db.add(event)

    db.commit()

    db.refresh(event)


    return event
