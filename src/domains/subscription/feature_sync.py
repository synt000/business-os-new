import json

from sqlalchemy.orm import Session

from src.models.saas_core import TenantFeature
from src.domains.subscription.models import SubscriptionPlan


def sync_plan_features_to_tenant(
    db: Session,
    tenant_id: str,
    plan_id: str,
):
    plan = (
        db.query(SubscriptionPlan)
        .filter(
            SubscriptionPlan.id == plan_id,
            SubscriptionPlan.active == True
        )
        .first()
    )

    if not plan:
        raise Exception("SUBSCRIPTION_PLAN_NOT_FOUND")


    try:
        features = json.loads(plan.features_json or "{}")
    except Exception:
        features = {}


    feature_codes = features.get("features", [])


    for code in feature_codes:

        exists = (
            db.query(TenantFeature)
            .filter(
                TenantFeature.tenant_id == tenant_id,
                TenantFeature.feature_code == code
            )
            .first()
        )

        if exists:
            exists.enabled = True
            continue


        db.add(
            TenantFeature(
                tenant_id=tenant_id,
                feature_code=code,
                enabled=True
            )
        )


    db.commit()

    return feature_codes
