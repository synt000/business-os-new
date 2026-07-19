from datetime import datetime

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user
from src.domains.subscription.models import Subscription
from src.models.saas_core import User


PUBLIC_PATHS = [
    "/login",
    "/register",
    "/token",
    "/docs",
    "/openapi.json",
    "/public",
]


def check_trial_access(
    db: Session,
    tenant_id: str
):
    subscription = (
        db.query(Subscription)
        .filter(
            Subscription.tenant_id == tenant_id,
            Subscription.status == "ACTIVE"
        )
        .first()
    )

    if not subscription:
        return False

    if subscription.end_date:
        if subscription.end_date < datetime.utcnow():
            subscription.status = "EXPIRED"
            db.commit()
            return False

    return True


def require_active_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    allowed = check_trial_access(
        db,
        current_user.tenant_id
    )

    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "TRIAL_EXPIRED",
                "message": "Your subscription expired. Please enter activation key."
            }
        )

    return current_user
