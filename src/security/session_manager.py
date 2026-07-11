from datetime import datetime

from sqlalchemy.orm import Session

from src.models.login_session import LoginSession


def create_login_session(
    db: Session,
    user,
    ip_address: str = "UNKNOWN",
    user_agent: str = "UNKNOWN",
    device_name: str = "UNKNOWN",
    refresh_jti: str | None = None,
):
    session = LoginSession(
        tenant_id=user.tenant_id,
        user_id=user.id,
        ip_address=ip_address,
        user_agent=user_agent,
        device_name=device_name,
        refresh_jti=refresh_jti,
        login_at=datetime.utcnow(),
        last_seen=datetime.utcnow(),
        is_active=True,
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


def update_last_seen(db: Session, session_id: int):
    session = db.query(LoginSession).filter(
        LoginSession.id == session_id
    ).first()

    if session:
        session.last_seen = datetime.utcnow()
        db.commit()


def logout_session(db: Session, session_id: int):
    session = db.query(LoginSession).filter(
        LoginSession.id == session_id
    ).first()

    if session:
        session.is_active = False
        session.logout_at = datetime.utcnow()
        db.commit()


def logout_all_sessions(db: Session, user_id: str):
    sessions = db.query(LoginSession).filter(
        LoginSession.user_id == user_id,
        LoginSession.is_active == True
    ).all()

    for s in sessions:
        s.is_active = False
        s.logout_at = datetime.utcnow()

    db.commit()
