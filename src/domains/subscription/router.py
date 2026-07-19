from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.core.security import get_current_user

from src.domains.subscription.schemas import (
    SubscriptionPlanCreate,
    SubscriptionPlanResponse,
    StartSubscriptionRequest,
    SubscriptionResponse,
    SubscriptionPaymentCreate,
    SubscriptionPaymentResponse
)

from src.domains.subscription.service import (
    create_plan,
    create_subscription,
    create_subscription_payment,
    confirm_subscription_payment
)

from src.domains.subscription.models import (
    SubscriptionPlan,
    Subscription
)


router = APIRouter(
    prefix="/subscription",
    tags=["Subscription"]
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

