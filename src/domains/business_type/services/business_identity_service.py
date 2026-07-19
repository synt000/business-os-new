from sqlalchemy.orm import Session

from src.models.saas_core import (
    Tenant,
    TenantFeature,
    BusinessType,
)


def get_business_identity(
    db: Session,
    tenant_id: str
):

    tenant = (
        db.query(Tenant)
        .filter(
            Tenant.id == tenant_id
        )
        .first()
    )

    if not tenant:
        return {
            "status": "FAILED",
            "message": "TENANT_NOT_FOUND"
        }


    business_type = None

    if tenant.business_type_id:

        business_type = (
            db.query(BusinessType)
            .filter(
                BusinessType.id == tenant.business_type_id
            )
            .first()
        )


    features = (
        db.query(TenantFeature)
        .filter(
            TenantFeature.tenant_id == tenant_id,
            TenantFeature.enabled == True
        )
        .all()
    )


    return {

        "status": "SUCCESS",

        "company": {
            "id": tenant.id,
            "name": tenant.company_name
        },


        "business": {

            "type_id": (
                business_type.id
                if business_type
                else None
            ),

            "type_code": (
                business_type.code
                if business_type
                else None
            ),

            "type_name": (
                business_type.name
                if business_type
                else None
            )

        },


        "features": [

            x.feature_code

            for x in features

        ]

    }
