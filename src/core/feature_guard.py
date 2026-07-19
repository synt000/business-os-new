from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user
from src.models.saas_core import User, TenantFeature


def require_feature(feature_code: str):

    def feature_checker(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):

        feature = (
            db.query(TenantFeature)
            .filter(
                TenantFeature.tenant_id == current_user.tenant_id,
                TenantFeature.feature_code == feature_code,
                TenantFeature.enabled == True
            )
            .first()
        )

        if not feature:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "FEATURE_LOCKED",
                    "feature": feature_code
                }
            )

        return True

    return feature_checker
