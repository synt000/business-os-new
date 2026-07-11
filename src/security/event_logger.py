from fastapi import Request
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
    description: str | None = None,
    severity: str = "INFO"
):

    ip_address = None
    user_agent = None


    if request:

        ip_address = get_client_ip(request)

        user_agent = request.headers.get(
            "user-agent",
            "UNKNOWN"
        )


    event = SecurityEvent(

        user_id=user_id,

        tenant_id=tenant_id,

        event_type=event_type,

        severity=severity,

        ip_address=ip_address,

        user_agent=user_agent,

        description=description
    )


    db.add(event)

    db.commit()

    db.refresh(event)


    return event
