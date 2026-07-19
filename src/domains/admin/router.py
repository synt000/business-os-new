from src.domains.permissions.audit_model import PermissionAuditLog
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from . import service
from .schemas import (
    TenantStatusUpdate,
    PlanCreate,
    PlanUpdate,
)


router = APIRouter(
    prefix="/admin",
    tags=["Admin SaaS"]
)


@router.get("/health")
def admin_health():
    return {
        "module": "admin",
        "status": "ready"
    }


@router.get("/tenants")
def tenants(db: Session = Depends(get_db)):
    data = service.list_tenants(db)

    return [
        {
            "id": t.id,
            "company_name": t.company_name,
            "owner_email": t.owner_email,
            "subscription_tier": t.subscription_tier,
            "billing_active": t.is_billing_active
        }
        for t in data
    ]


@router.get("/tenants/{tenant_id}")
def tenant_detail(
    tenant_id: str,
    db: Session = Depends(get_db)
):
    tenant = service.get_tenant(db, tenant_id)

    if not tenant:
        raise HTTPException(
            status_code=404,
            detail="Tenant not found"
        )

    return {
        "id": tenant.id,
        "company_name": tenant.company_name,
        "owner_email": tenant.owner_email,
        "subscription_tier": tenant.subscription_tier,
        "billing_active": tenant.is_billing_active
    }


@router.post("/tenants/{tenant_id}/billing")
def billing_update(
    tenant_id: str,
    payload: TenantStatusUpdate,
    db: Session = Depends(get_db)
):
    tenant = service.update_billing_status(
        db,
        tenant_id,
        payload.is_billing_active
    )

    if not tenant:
        raise HTTPException(
            status_code=404,
            detail="Tenant not found"
        )

    return {
        "status": "updated",
        "tenant_id": tenant.id,
        "billing_active": tenant.is_billing_active
    }


# ======================================
# OWNER ADMIN PERMISSION MANAGEMENT API
# ======================================

from src.core.permissions.guard import require_permission
from src.models.saas_core import User
from src.domains.permissions.models import (
    UserPermission,
    Permission
)


@router.get("/users")
def owner_list_admins(
    db: Session = Depends(get_db)
):
    from src.domains.admin.service import list_admins

    admins = list_admins(db)

    return [
        {
            "id": a.id,
            "email": a.email,
            "role": a.role
        }
        for a in admins
    ]


@router.get("/users/{user_id}/permissions")
def owner_user_permissions(
    user_id: str,
    db: Session = Depends(get_db)
):

    rows = (
        db.query(Permission)
        .join(
            UserPermission,
            UserPermission.permission_id == Permission.id
        )
        .filter(
            UserPermission.user_id == user_id
        )
        .all()
    )


    return {
        "user_id": user_id,
        "permissions":[
            {
                "id": p.id,
                "code": p.code
            }
            for p in rows
        ]
    }



@router.post(
    "/users/{user_id}/permissions/{permission_id}"
)
def owner_add_permission(
    user_id:str,
    permission_id:int,
    db:Session = Depends(get_db)
):

    exists = (
        db.query(UserPermission)
        .filter(
            UserPermission.user_id == user_id,
            UserPermission.permission_id == permission_id
        )
        .first()
    )


    if exists:
        return {
            "status":"EXISTS"
        }


    row = UserPermission(
        user_id=user_id,
        permission_id=permission_id
    )

    db.add(row)


    audit = PermissionAuditLog(
        actor_user_id="OWNER",
        target_user_id=user_id,
        permission_id=permission_id,
        action="GRANTED"
    )

    db.add(audit)

    db.commit()


    return {
        "status":"SUCCESS"
    }



@router.delete(
    "/users/{user_id}/permissions/{permission_id}"
)
def owner_remove_permission(
    user_id:str,
    permission_id:int,
    db:Session = Depends(get_db)
):

    row = (
        db.query(UserPermission)
        .filter(
            UserPermission.user_id == user_id,
            UserPermission.permission_id == permission_id
        )
        .first()
    )


    if row:

        db.delete(row)


    audit = PermissionAuditLog(
        actor_user_id="OWNER",
        target_user_id=user_id,
        permission_id=permission_id,
        action="REMOVED"
    )


    db.add(audit)

    db.commit()


    return {
        "status":"SUCCESS"
    }



# ======================================
# PERMISSION AUDIT HISTORY API
# ======================================

@router.get(
    "/users/{user_id}/permission-history"
)
def permission_history(
    user_id: str,
    db: Session = Depends(get_db)
):

    logs = (
        db.query(PermissionAuditLog)
        .filter(
            PermissionAuditLog.target_user_id == user_id
        )
        .order_by(
            PermissionAuditLog.id.desc()
        )
        .all()
    )


    history = []

    for log in logs:

        permission = (
            db.query(Permission)
            .filter(
                Permission.id == log.permission_id
            )
            .first()
        )

        history.append(
            {
                "permission_id": log.permission_id,
                "permission_code": (
                    permission.code
                    if permission
                    else "unknown"
                ),
                "action": log.action,
                "created_at": log.created_at
            }
        )


    return {
        "user_id": user_id,
        "history": history
    }


# ======================================
# SUBSCRIPTION PLAN MANAGEMENT API
# ======================================

from .schemas import PlanCreate, PlanUpdate


@router.post("/plans")
def admin_create_plan(
    payload: PlanCreate,
    db: Session = Depends(get_db)
):
    return service.create_plan(db, payload)


@router.get("/plans")
def admin_list_plans(
    db: Session = Depends(get_db)
):
    plans = service.list_plans(db)

    return [
        {
            "id": p.id,
            "name": p.name,
            "duration_days": p.duration_days,
            "price": p.price,
            "features": __import__("json").loads(
                p.features_json or "{}"
            ).get("features", []),
            "active": p.active,
        }
        for p in plans
    ]


@router.get("/plans/{plan_id}")
def admin_get_plan(
    plan_id: str,
    db: Session = Depends(get_db)
):
    plan = service.get_plan(db, plan_id)

    if not plan:
        raise HTTPException(
            status_code=404,
            detail="PLAN_NOT_FOUND"
        )

    return plan


@router.put("/plans/{plan_id}")
def admin_update_plan(
    plan_id: str,
    payload: PlanUpdate,
    db: Session = Depends(get_db)
):
    plan = service.update_plan(
        db,
        plan_id,
        payload
    )

    if not plan:
        raise HTTPException(
            status_code=404,
            detail="PLAN_NOT_FOUND"
        )

    return plan


@router.delete("/plans/{plan_id}")
def admin_disable_plan(
    plan_id: str,
    db: Session = Depends(get_db)
):
    plan = service.disable_plan(
        db,
        plan_id
    )

    if not plan:
        raise HTTPException(
            status_code=404,
            detail="PLAN_NOT_FOUND"
        )

    return {
        "status": "DISABLED",
        "plan_id": plan.id
    }
