from src.core.database import SessionLocal

from src.domains.business_type.services.feature_assign_service import (
    assign_features_to_tenant
)


db = SessionLocal()


tenant_id = "e4ca6dc4-9543-4c4f-ab8c-a39777f27b45"


business_type_id = "b83574dd-172e-4f03-bb72-361255b29497"


features = assign_features_to_tenant(
    db,
    tenant_id,
    business_type_id
)


print(
    "Assigned:",
    features
)

db.close()
