from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user

from src.models.saas_core import User

from src.domains.ai_insight.service import (
    generate_business_insights
)

from src.domains.ai_insight.recommendation import (
    generate_ai_recommendations
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
