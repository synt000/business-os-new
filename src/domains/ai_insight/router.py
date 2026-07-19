from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user
from src.core.features.guard import check_feature

from src.models.saas_core import User

from src.domains.ai_insight.service import (
    generate_business_insights,
    generate_ceo_daily_brief,
    generate_profit_margin_insight
)

from src.domains.ai_insight.recommendation import (
    generate_ai_recommendations
)

from src.domains.ai_insight.action_service import (
    generate_ai_actions,
    execute_ai_action
)

from src.domains.ai_insight.service import (
    generate_ceo_score,
    create_ai_purchase_order
)



def verify_ai_feature(db, user):
    check_feature(
        db,
        user.tenant_id,
        "AI_INSIGHT"
    )


router = APIRouter(
    prefix="/ai",
    tags=["AI Insight"]
)


@router.get("/insights")
def insights(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    check_feature(
        db,
        current_user.tenant_id,
        "AI_INSIGHT"
    )

    return generate_business_insights(
        db,
        current_user.tenant_id
    )


@router.get("/recommendations")
def recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    check_feature(
        db,
        current_user.tenant_id,
        "AI_INSIGHT"
    )

    return generate_ai_recommendations(
        db,
        current_user.tenant_id
    )


@router.get("/profit-margin")
def profit_margin(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    check_feature(
        db,
        current_user.tenant_id,
        "AI_INSIGHT"
    )

    return generate_profit_margin_insight(
        db,
        current_user.tenant_id
    )



@router.get("/ceo-brief")
def ceo_daily_brief(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    check_feature(
        db,
        current_user.tenant_id,
        "AI_INSIGHT"
    )

    return generate_ceo_daily_brief(
        db,
        current_user.tenant_id
    )


@router.get("/ceo-score")
def ceo_score(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    check_feature(
        db,
        current_user.tenant_id,
        "AI_INSIGHT"
    )

    return generate_ceo_score(
        db,
        current_user.tenant_id
    )


@router.post("/create-purchase-order")
def create_purchase_order(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    check_feature(
        db,
        current_user.tenant_id,
        "AI_INSIGHT"
    )

    return create_ai_purchase_order(
        db,
        current_user.tenant_id
    )



# =========================
# AI INSIGHT HISTORY
# =========================

@router.get("/history")
def ai_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    from src.models.saas_core import AIInsight

    records = (
        db.query(AIInsight)
        .filter(
            AIInsight.tenant_id == current_user.tenant_id
        )
        .order_by(
            AIInsight.created_at.desc()
        )
        .limit(50)
        .all()
    )


    return [
        {
            "id": x.id,
            "title": x.title,
            "message": x.message,
            "priority": x.priority,
            "created_at": x.created_at
        }
        for x in records
    ]



@router.get("/actions")
def ai_actions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return generate_ai_actions(
        db,
        current_user.tenant_id
    )


@router.post("/actions/{action_id}")
def run_ai_action(
    action_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return execute_ai_action(
        db,
        current_user.tenant_id,
        current_user.id,
        action_id
    )


# ==========================================
# AI ACTION EXECUTE
# ==========================================

@router.post("/actions/{action_id}/execute")
def execute_action(
    action_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return execute_ai_action(
        db,
        current_user.tenant_id,
        current_user.id,
        action_id
    )



# ==========================================
# AI PROCUREMENT APPROVAL DASHBOARD
# ==========================================

from src.domains.purchase.models import PurchaseOrder


@router.get("/purchases/pending")
def get_pending_ai_purchases(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    rows = (
        db.query(PurchaseOrder)
        .filter(
            PurchaseOrder.tenant_id == current_user.tenant_id,
            PurchaseOrder.status == "PENDING_APPROVAL"
        )
        .order_by(
            PurchaseOrder.created_at.desc()
        )
        .all()
    )

    return {
        "status": "SUCCESS",
        "count": len(rows),
        "items": [
            {
                "id": x.id,
                "purchase_number": x.purchase_number,
                "amount": x.total_amount,
                "status": x.status,
                "created_at": x.created_at
            }
            for x in rows
        ]
    }



# ==========================================
# AI PURCHASE ORDER REJECT
# ==========================================

from pydantic import BaseModel


class AIRejectPayload(BaseModel):
    reason: str


@router.post("/purchases/reject/{purchase_id}")
def reject_ai_purchase(
    purchase_id: str,
    data: AIRejectPayload,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    from src.domains.purchase.models import PurchaseOrder, AIActionLog


    po = (
        db.query(PurchaseOrder)
        .filter(
            PurchaseOrder.id == purchase_id,
            PurchaseOrder.tenant_id == current_user.tenant_id
        )
        .first()
    )


    if not po:
        return {
            "status":"FAILED",
            "message":"Purchase Order Not Found"
        }


    if po.status == "RECEIVED":
        return {
            "status":"FAILED",
            "message":"PURCHASE_ALREADY_RECEIVED"
        }


    po.status = "REJECTED"


    log = AIActionLog(
        tenant_id=current_user.tenant_id,
        user_id=current_user.id,
        action_id="CREATE_PURCHASE_ORDER",
        action_title="AI Purchase Order Rejected",
        status="FAILED",
        result_message=data.reason
    )

    db.add(log)
    db.commit()


    return {
        "status":"SUCCESS",
        "message":"AI Purchase Order Rejected",
        "purchase_number":po.purchase_number,
        "reason":data.reason
    }
