from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from src.core.database import get_db
from src.core.security import get_current_user
from src.models.saas_core import User
from src.domains.subscription.models import Subscription


def require_active_subscription():

    def checker(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):

        subscription = (
            db.query(Subscription)
            .filter(
                Subscription.tenant_id == current_user.tenant_id,
                Subscription.status == "ACTIVE"
            )
            .first()
        )

        if not subscription:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="ACTIVE_SUBSCRIPTION_REQUIRED"
            )

        if subscription.end_date < datetime.utcnow():
            subscription.status = "EXPIRED"
            db.commit()

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="SUBSCRIPTION_EXPIRED"
            )

        return current_user

    return checker
