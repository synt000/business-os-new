from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.saas_core import TenantFeature


def check_feature(
    db: Session,
    tenant_id: str,
    feature_code: str
):
    feature = (
        db.query(TenantFeature)
        .filter(
            TenantFeature.tenant_id == tenant_id,
            TenantFeature.feature_code == feature_code,
            TenantFeature.enabled == True
        )
        .first()
    )

    if not feature:
        raise HTTPException(
            status_code=403,
            detail=f"FEATURE_LOCKED:{feature_code}"
        )

    return True
