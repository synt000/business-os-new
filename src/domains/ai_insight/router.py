from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user

from src.models.saas_core import User

from src.domains.ai_insight.service import (
    generate_business_insights,
    generate_ceo_daily_brief,
    generate_profit_margin_insight
)

from src.domains.ai_insight.recommendation import (
    generate_ai_recommendations
)

from src.domains.ai_insight.service import (
    generate_ceo_score,
    create_ai_purchase_order
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

    return generate_business_insights(
        db,
        current_user.tenant_id
    )


@router.get("/recommendations")
def recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return generate_ai_recommendations(
        db,
        current_user.tenant_id
    )


@router.get("/profit-margin")
def profit_margin(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return generate_profit_margin_insight(
        db,
        current_user.tenant_id
    )



@router.get("/ceo-brief")
def ceo_daily_brief(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return generate_ceo_daily_brief(
        db,
        current_user.tenant_id
    )


@router.get("/ceo-score")
def ceo_score(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return generate_ceo_score(
        db,
        current_user.tenant_id
    )


@router.post("/create-purchase-order")
def create_purchase_order(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return create_ai_purchase_order(
        db,
        current_user.tenant_id
    )

