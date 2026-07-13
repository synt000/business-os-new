from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user
from src.models.saas_core import User

from src.domains.dashboard.service import (
    get_dashboard_menus,
    get_ceo_dashboard_summary,
    get_business_health_score,
    get_sales_trend,
    get_revenue_expense_summary,
)

from src.domains.dashboard.schemas import (
    DashboardMenuResponse
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get(
    "/menus",
    response_model=list[DashboardMenuResponse]
)
def dashboard_menus(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_dashboard_menus(
        db,
        current_user.tenant_id
    )


@router.get("/ceo-summary")
def ceo_dashboard_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return {
        "status": "SUCCESS",
        "dashboard": get_ceo_dashboard_summary(
            db,
            current_user.tenant_id
        )
    }


@router.get("/business-health")
def business_health(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return {
        "status": "SUCCESS",
        "health": get_business_health_score(
            db,
            current_user.tenant_id
        )
    }


@router.get("/executive-ai")
def executive_ai(
    current_user: User = Depends(get_current_user)
):
    return {
        "status": "SUCCESS",
        "assistant": "Business OS AI",
        "message": "Business analysis ready."
    }


@router.get("/sales-trend")
def sales_trend(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return {
        "status": "SUCCESS",
        "trend": get_sales_trend(
            db,
            current_user.tenant_id
        )
    }


@router.get("/revenue-expense")
def revenue_expense(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return {
        "status": "SUCCESS",
        "summary": get_revenue_expense_summary(
            db,
            current_user.tenant_id
        )
    }
