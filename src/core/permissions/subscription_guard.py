from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from src.core.database import get_db
from src.core.security import get_current_user
from src.models.saas_core import User, Tenant
from src.domains.subscription.models import Subscription


def require_active_subscription():

    def checker(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):

        tenant = (
            db.query(Tenant)
            .filter(
                Tenant.id == current_user.tenant_id
            )
            .first()
        )

        if not tenant:
            raise HTTPException(
                status_code=404,
                detail="TENANT_NOT_FOUND"
            )


        # FREE TRIAL MODE
        if tenant.subscription_tier.value == "FREE_TRIAL":

            if tenant.trial_expired:
                raise HTTPException(
                    status_code=402,
                    detail="WORKSPACE_LOCKED: FREE_TRIAL_EXPIRED"
                )

            if not tenant.is_billing_active:
                raise HTTPException(
                    status_code=402,
                    detail="WORKSPACE_LOCKED: BILLING_DISABLED"
                )

            return current_user


        # PAID SUBSCRIPTION MODE

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
                status_code=403,
                detail="ACTIVE_SUBSCRIPTION_REQUIRED"
            )


        if subscription.end_date < datetime.utcnow():

            subscription.status = "EXPIRED"
            db.commit()

            raise HTTPException(
                status_code=402,
                detail="SUBSCRIPTION_EXPIRED"
            )


        return current_user


    return checker
