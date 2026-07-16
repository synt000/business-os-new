from fastapi import APIRouter, Depends
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
    return create_subscription_payment(
        db,
        current_user.tenant_id,
        payload.plan_id,
        payload.method,
        payload.transaction_ref
    )


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
