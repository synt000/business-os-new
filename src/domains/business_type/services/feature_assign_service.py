from sqlalchemy.orm import Session

import uuid

from src.models.saas_core import (
    TenantFeature,
    BusinessType,
)

from src.domains.business_type.feature_mapping import (
    FEATURE_MAPPING,
)


def assign_features_to_tenant(
    db: Session,
    tenant_id: str,
    business_type_id: str,
):

    business_type = (
        db.query(BusinessType)
        .filter(
            BusinessType.id == business_type_id
        )
        .first()
    )


    if not business_type:
        raise Exception(
            "BUSINESS_TYPE_NOT_FOUND"
        )


    features = FEATURE_MAPPING.get(
        business_type.code,
        []
    )


    for feature in features:

        exists = (
            db.query(TenantFeature)
            .filter(
                TenantFeature.tenant_id == tenant_id,
                TenantFeature.feature_code == feature
            )
            .first()
        )


        if exists:
            continue


        tenant_feature = TenantFeature(
            id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            feature_code=feature,
            enabled=True,
        )


        db.add(
            tenant_feature
        )


    db.commit()


    return features
