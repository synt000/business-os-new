from src.models.saas_core import BusinessFeature
from src.domains.subscription.models import TenantSubscription


def tenant_has_feature(db, tenant_id, feature_code):

    subscription = (
        db.query(TenantSubscription)
        .filter(
            TenantSubscription.tenant_id == tenant_id
        )
        .first()
    )

    if not subscription:
        return False


    feature = (
        db.query(BusinessFeature)
        .filter(
            BusinessFeature.business_type_id == subscription.business_type_id,
            BusinessFeature.feature_code == feature_code,
            BusinessFeature.enabled == True
        )
        .first()
    )

    return feature is not None



def get_tenant_features(db, tenant_id):

    subscription = (
        db.query(TenantSubscription)
        .filter(
            TenantSubscription.tenant_id == tenant_id
        )
        .first()
    )

    if not subscription:
        return []


    features = (
        db.query(BusinessFeature)
        .filter(
            BusinessFeature.business_type_id == subscription.business_type_id,
            BusinessFeature.enabled == True
        )
        .all()
    )

    return [
        x.feature_code
        for x in features
    ]
