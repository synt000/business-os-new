from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user

from src.domains.finance.service import (
    get_finance_summary,
    get_finance_health_score,
)


router = APIRouter(
    prefix="/finance",
    tags=["Finance"]
)


@router.get("/summary")
def finance_summary(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return get_finance_summary(
        db,
        current_user.tenant_id
    )


@router.get("/health")
def finance_health(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return get_finance_health_score(
        db,
        current_user.tenant_id
    )
