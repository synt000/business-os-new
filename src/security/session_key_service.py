import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from src.models.login_session import LoginSession


def create_user_session(
    db: Session,
    user,
    request=None
):

    session_key = str(uuid.uuid4())


    session = LoginSession(
        user_id=user.id,
        tenant_id=user.tenant_id,
        session_key=session_key,
        device_name=(
            request.headers.get("user-agent")
            if request
            else "UNKNOWN"
        ),
        ip_address=(
            request.client.host
            if request and request.client
            else "UNKNOWN"
        ),
        is_active=True,
        last_used_at=datetime.utcnow()
    )


    db.add(session)
    db.commit()
    db.refresh(session)


    return session_key
