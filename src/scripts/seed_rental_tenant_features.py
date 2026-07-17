from src.core.database import SessionLocal
from src.models.saas_core import (
    Tenant,
    TenantFeature,
    BusinessType,
    BusinessFeature,
)

db = SessionLocal()

tenant = (
    db.query(Tenant)
    .filter(Tenant.company_name=="Test Rental Shop")
    .first()
)

if not tenant:
    print("Tenant not found")
    exit()


business_type = (
    db.query(BusinessType)
    .filter(BusinessType.code=="RENTAL_SERVICE")
    .first()
)

if not business_type:
    print("Business Type not found")
    exit()


features = (
    db.query(BusinessFeature)
    .filter(
        BusinessFeature.business_type_id == business_type.id
    )
    .all()
)


for feature in features:

    exists = (
        db.query(TenantFeature)
        .filter(
            TenantFeature.tenant_id == tenant.id,
            TenantFeature.feature_code == feature.feature_code
        )
        .first()
    )

    if not exists:
        db.add(
            TenantFeature(
                tenant_id=tenant.id,
                feature_code=feature.feature_code,
                enabled=True
            )
        )


db.commit()

print("✓ Rental Tenant Features Seeded")

db.close()
