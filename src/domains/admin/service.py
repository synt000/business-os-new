from sqlalchemy.orm import Session

from src.models.saas_core import Tenant


def list_tenants(db: Session):
    return db.query(Tenant).all()


def get_tenant(db: Session, tenant_id: str):
    return (
        db.query(Tenant)
        .filter(Tenant.id == tenant_id)
        .first()
    )


def update_billing_status(
    db: Session,
    tenant_id: str,
    active: bool
):
    tenant = get_tenant(db, tenant_id)

    if not tenant:
        return None

    tenant.is_billing_active = active
    db.commit()
    db.refresh(tenant)

    return tenant


# =====================================
# ADMIN USER MANAGEMENT
# =====================================

def list_admins(db: Session):

    from src.models.saas_core import User

    return (
        db.query(User)
        .filter(
            User.role.in_(
                [
                    "ADMIN",
                    "OWNER"
                ]
            )
        )
        .all()
    )



def create_admin(
    db: Session,
    admin
):

    from src.models.saas_core import User
    from src.core.security import hash_password
    import uuid


    user = User(
        id=str(uuid.uuid4()),
        email=admin.email,
        username=getattr(admin, "username", admin.email),
        hashed_password=hash_password(
            admin.password
        ),
        role="ADMIN"
    )


    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# =====================================
# SUBSCRIPTION PLAN MANAGEMENT
# =====================================

import json
import uuid

from src.domains.subscription.models import SubscriptionPlan


def create_plan(db: Session, data):
    plan = SubscriptionPlan(
        id=str(uuid.uuid4()),
        name=data.name,
        duration_days=data.duration_days,
        price=data.price,
        features_json=json.dumps({
            "features": data.features
        }),
        active=True
    )

    db.add(plan)
    db.commit()
    db.refresh(plan)

    return plan


def list_plans(db: Session):
    return db.query(SubscriptionPlan).all()


def get_plan(db: Session, plan_id: str):
    return (
        db.query(SubscriptionPlan)
        .filter(SubscriptionPlan.id == plan_id)
        .first()
    )


def update_plan(db: Session, plan_id: str, data):
    plan = get_plan(db, plan_id)

    if not plan:
        return None

    if data.name is not None:
        plan.name = data.name

    if data.duration_days is not None:
        plan.duration_days = data.duration_days

    if data.price is not None:
        plan.price = data.price

    if data.features is not None:
        plan.features_json = json.dumps({
            "features": data.features
        })

    if data.active is not None:
        plan.active = data.active

    db.commit()
    db.refresh(plan)

    return plan


def disable_plan(db: Session, plan_id: str):
    plan = get_plan(db, plan_id)

    if not plan:
        return None

    plan.active = False

    db.commit()
    db.refresh(plan)

    return plan


# =====================================
# PLAN FEATURE ASSIGNMENT
# =====================================

def assign_plan_features(db: Session, plan_id: str, features):

    plan = get_plan(db, plan_id)

    if not plan:
        return None

    import json

    plan.features_json = json.dumps({
        "features": features
    })

    db.commit()
    db.refresh(plan)

    return plan
