import uuid
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.database import get_db
from src.core.security import get_current_user

from src.domains.subscription.schemas import (
    SubscriptionPlanCreate,
    SubscriptionPlanResponse,
    StartSubscriptionRequest,
    SubscriptionResponse,
    SubscriptionPaymentCreate,
    SubscriptionPaymentResponse,
    ActivationRequest,
    ActivationKeyGenerateRequest
)

from src.domains.subscription.service import (
    create_plan,
    create_subscription,
    create_subscription_payment,
    confirm_subscription_payment
)

from src.domains.subscription.activation_service import activate_key

from src.domains.subscription.models import (
    SubscriptionPlan,
    Subscription,
    ActivationKey
)


templates = Jinja2Templates(directory="src/templates")

router = APIRouter(
    prefix="/subscription",
    tags=["Subscription"]
)


@router.get(
    "/activate",
    response_class=HTMLResponse
)
def activation_page(
    request: Request
):
    return templates.TemplateResponse(
        "subscription_locked.html",
        {
            "request": request
        }
    )



@router.post(
    "/plans",
    response_model=SubscriptionPlanResponse
)
def add_plan(
    payload: SubscriptionPlanCreate,
    db: Session = Depends(get_db)
):
    return create_plan(db, payload)



@router.get(
    "/plans",
    response_model=list[SubscriptionPlanResponse]
)
def list_plans(
    db: Session = Depends(get_db)
):
    return db.query(SubscriptionPlan).all()



@router.post(
    "/start",
    response_model=SubscriptionResponse
)
def start_subscription(
    payload: StartSubscriptionRequest,
    db: Session = Depends(get_db)
):
    return create_subscription(
        db,
        payload.tenant_id,
        payload.plan_id,
        payload.is_trial
    )



@router.get(
    "/tenant/{tenant_id}",
    response_model=list[SubscriptionResponse]
)
def tenant_subscriptions(
    tenant_id: str,
    db: Session = Depends(get_db)
):
    return (
        db.query(Subscription)
        .filter(
            Subscription.tenant_id == tenant_id
        )
        .all()
    )


@router.post(
    "/payment/create",
    response_model=SubscriptionPaymentResponse
)
def create_subscription_payment_api(
    payload: SubscriptionPaymentCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        return create_subscription_payment(
            db,
            current_user.tenant_id,
            payload.plan_id,
            payload.method,
            payload.transaction_ref
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail={
                "code": str(e),
                "message": str(e)
            }
        )
        if str(e) == "DUPLICATE_TRANSACTION_REFERENCE":
            raise HTTPException(
                status_code=400,
                detail={
                    "code": "DUPLICATE_TRANSACTION_REFERENCE",
                    "message": "Transaction reference already exists"
                }
            )

        if str(e) == "PLAN_NOT_FOUND":
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "PLAN_NOT_FOUND",
                    "message": "Subscription plan not found"
                }
            )

        raise


@router.post(
    "/payment/{payment_id}/confirm",
    response_model=SubscriptionPaymentResponse
)
def confirm_subscription_payment_api(
    payment_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return confirm_subscription_payment(
        db,
        payment_id
    )


# ======================================
# OWNER SUBSCRIPTION STATUS API
# ======================================

@router.get("/status/{tenant_id}")
def subscription_status(
    tenant_id: str,
    db: Session = Depends(get_db)
):
    subscription = (
        db.query(Subscription)
        .filter(
            Subscription.tenant_id == tenant_id,
            Subscription.status == "ACTIVE"
        )
        .first()
    )

    if not subscription:
        raise HTTPException(
            status_code=404,
            detail="ACTIVE_SUBSCRIPTION_NOT_FOUND"
        )

    plan = (
        db.query(SubscriptionPlan)
        .filter(
            SubscriptionPlan.id == subscription.plan_id
        )
        .first()
    )

    return {
        "tenant_id": tenant_id,
        "subscription_id": subscription.id,
        "status": subscription.status,
        "is_trial": subscription.is_trial,
        "start_date": subscription.start_date,
        "end_date": subscription.end_date,
        "plan": {
            "id": plan.id if plan else None,
            "name": plan.name if plan else None,
            "price": plan.price if plan else None
        }
    }


@router.post("/upgrade")
def upgrade_subscription(
    tenant_id: str,
    plan_id: str,
    db: Session = Depends(get_db)
):

    old = (
        db.query(Subscription)
        .filter(
            Subscription.tenant_id == tenant_id,
            Subscription.status == "ACTIVE"
        )
        .first()
    )

    if old:
        old.status = "CANCELLED"

    new_subscription = create_subscription(
        db,
        tenant_id,
        plan_id,
        False
    )

    return {
        "status": "UPGRADED",
        "subscription_id": new_subscription.id,
        "plan_id": plan_id
    }



@router.get(
    "/keys",
    response_model=list[dict]
)
def list_activation_keys(
    db: Session = Depends(get_db)
):
    keys = db.query(ActivationKey).all()

    result = []

    for k in keys:
        plan = (
            db.query(SubscriptionPlan)
            .filter(SubscriptionPlan.id == k.plan_id)
            .first()
        )

        result.append({
            "key_code": k.key_code,
            "plan_id": k.plan_id,
            "plan_name": plan.name if plan else "UNKNOWN",
            "duration_days": k.duration_days,
            "status": "USED" if k.used else "AVAILABLE",
            "used": k.used,
            "tenant_id": k.tenant_id,
            "used_at": str(k.used_at) if k.used_at else None
        })

    return result


@router.post(
    "/key/generate",
    response_model=dict
)
def generate_activation_key(
    payload: ActivationKeyGenerateRequest,
    db: Session = Depends(get_db)
):

    # FREE TRIAL DOES NOT USE ACTIVATION KEY
    FREE_TRIAL_PLAN_ID = "ea854e50-db99-4496-bdec-ac9683a77839"

    if payload.plan_id == FREE_TRIAL_PLAN_ID:
        raise HTTPException(
            status_code=400,
            detail="FREE_TRIAL_KEY_NOT_ALLOWED"
        )

    key_code = "ACT-" + uuid.uuid4().hex[:8].upper()

    key = ActivationKey(
        id=str(uuid.uuid4()),
        key_code=key_code,
        plan_id=payload.plan_id,
        duration_days=payload.duration_days,
        used=False
    )

    db.add(key)
    db.commit()
    db.refresh(key)

    return {
        "status": "SUCCESS",
        "key": key.key_code,
        "duration_days": key.duration_days,
        "plan_id": key.plan_id
    }



@router.post(
    "/key/revoke/{key_code}",
    response_model=dict
)
def revoke_activation_key(
    key_code: str,
    db: Session = Depends(get_db)
):

    key = (
        db.query(ActivationKey)
        .filter(
            ActivationKey.key_code == key_code
        )
        .first()
    )

    if not key:
        raise HTTPException(
            status_code=404,
            detail="KEY_NOT_FOUND"
        )

    key.status = "REVOKED"

    db.commit()

    return {
        "status": "SUCCESS",
        "key": key.key_code,
        "message": "Activation key revoked"
    }


@router.post(
    "/activate",
    response_model=dict
)
def activate_subscription_key(
    payload: ActivationRequest,
    db: Session = Depends(get_db)
):
    try:
        result = activate_key(
            db,
            payload.key_code,
            payload.tenant_id
        )

        return {
            "status": "SUCCESS",
            "message": "Subscription activated",
            "data": {
                "subscription_id": result.id,
                "tenant_id": result.tenant_id,
                "status": result.status,
                "start_date": str(result.start_date),
                "end_date": str(result.end_date)
            }
        }

    except Exception as e:
        if str(e) == "KEY_NOT_FOUND":
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "KEY_NOT_FOUND",
                    "message": "Activation key not found"
                }
            )

        if str(e) == "KEY_ALREADY_USED":
            raise HTTPException(
                status_code=400,
                detail={
                    "code": "KEY_ALREADY_USED",
                    "message": "Activation key already used"
                }
            )

        raise