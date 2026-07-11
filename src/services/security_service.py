from sqlalchemy.orm import Session

from src.models.security_log import SecurityLog


def create_security_log(
    db: Session,
    event: str,
    ip_address: str = None,
    user_agent: str = None,
    tenant_id: str = None,
    user_id: str = None,
    request_id: str = None
):

    log = SecurityLog(
        event=event,
        ip_address=ip_address,
        user_agent=user_agent,
        tenant_id=tenant_id,
        user_id=user_id,
        request_id=request_id
    )

    db.add(log)
    db.commit()

    return log
