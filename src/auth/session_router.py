from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user
from src.models.login_session import LoginSession
from src.models.saas_core import User
from src.security.session_manager import logout_all_sessions

router = APIRouter(
    prefix="/api/v4/auth",
    tags=["Session Management"]
)


@router.get("/sessions")
def get_active_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    sessions = (
        db.query(LoginSession)
        .filter(
            LoginSession.user_id == current_user.id,
            LoginSession.is_active == True
        )
        .order_by(LoginSession.login_at.desc())
        .all()
    )

    return [
        {
            "id": s.id,
            "ip_address": s.ip_address,
            "device_name": s.device_name,
            "user_agent": s.user_agent,
            "login_at": s.login_at,
            "last_seen": s.last_seen,
            "is_active": s.is_active,
        }
        for s in sessions
    ]


@router.post("/logout-all")
def logout_all(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    logout_all_sessions(db, current_user.id)

    return {
        "success": True,
        "message": "ALL_ACTIVE_SESSIONS_TERMINATED"
    }
