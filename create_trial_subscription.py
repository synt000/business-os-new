from datetime import datetime, timedelta

from src.core.database import SessionLocal

# load all models first
import src.models
import src.models.saas_core

from src.domains.subscription.models import (
    TenantSubscription,
    SubscriptionPlan
)

db = SessionLocal()

tenant_id = "0d3a21e3-7356-440f-bdb8-e5598516935d"

plan = (
    db.query(SubscriptionPlan)
    .filter(
        SubscriptionPlan.name=="FREE_TRIAL"
    )
    .first()
)

if not plan:
    print("FREE_TRIAL PLAN NOT FOUND")
    exit()


existing = (
    db.query(TenantSubscription)
    .filter(
        TenantSubscription.tenant_id == tenant_id
    )
    .first()
)

if existing:
    print("ALREADY EXISTS")
    print(existing.id)
    exit()


sub = TenantSubscription(
    tenant_id=tenant_id,
    business_type_id="29db1cf2-8fbd-4da5-907c-ef7dcf4dfa54",
    plan_id=plan.id,
    status="ACTIVE",
    start_date=datetime.utcnow(),
    expire_date=datetime.utcnow()+timedelta(days=3)
)


db.add(sub)
db.commit()
db.refresh(sub)

print("CREATED")
print("ID:", sub.id)
print("STATUS:", sub.status)
print("EXPIRE:", sub.expire_date)

db.close()
