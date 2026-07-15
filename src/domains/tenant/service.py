from datetime import datetime, timedelta
import uuid

from src.models.saas_core import Tenant


def create_tenant(db, name):

    tenant = Tenant(
        id=str(uuid.uuid4()),
        company_name=name,
        owner_email=f"owner@{name.lower().replace(' ', '')}.local",
        subscription_tier="FREE_TRIAL",
        is_billing_active=True,
        trial_expired=False,
        max_sku_limit=50,
        max_order_limit=100,
        enable_pos_feature=True,
        enable_ai_forecast=False
    )

    db.add(tenant)
    db.commit()
    db.refresh(tenant)

    return tenant
