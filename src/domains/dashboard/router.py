from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.services.dashboard_service import DashboardService
from src.core.security import get_current_user
from src.domains.trial.guard import require_active_subscription
from src.core.permissions import require_owner_role
from src.models.saas_core import User

from src.domains.dashboard.service import (
    get_dashboard_menus,
    get_ceo_dashboard_summary,
    get_business_health_score,
    get_sales_trend,
    get_revenue_expense_summary,
    get_financial_kpi_summary,
    get_finance_insight,
    get_owner_platform_summary,
    get_saas_revenue_summary,
    get_owner_renewal_summary,
)

from src.domains.social_center.service import get_social_summary

from src.domains.dashboard.schemas import (
    DashboardMenuResponse
)

templates = Jinja2Templates(directory="src/templates")


router = APIRouter(
    prefix="/owner",
    tags=["Owner Dashboard"]
)




@router.get("", response_class=HTMLResponse)
def owner_dashboard_page(
    request: Request
):
    return templates.TemplateResponse(
        "owner_dashboard.html",
        {
            "request": request,
            "user": None
        }
    )

@router.get(
    "/menus",
    response_model=list[DashboardMenuResponse]
)
def dashboard_menus(
    current_user: User = Depends(require_active_subscription),
    db: Session = Depends(get_db)
):
    return get_dashboard_menus(
        db,
        current_user.tenant_id
    )


@router.get("/ceo-summary")
def ceo_dashboard_summary(
    current_user: User = Depends(require_active_subscription),
    db: Session = Depends(get_db)
):
    return {
        "status": "SUCCESS",
        "dashboard": get_ceo_dashboard_summary(
            db,
            current_user.tenant_id
        ),
        "finance": get_finance_insight(
            db,
            current_user.tenant_id
        )
    }


@router.get("/business-health")
def business_health(
    current_user: User = Depends(require_active_subscription),
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
    current_user: User = Depends(require_active_subscription)
):
    return {
        "status": "SUCCESS",
        "assistant": "Business OS AI",
        "message": "Business analysis ready."
    }


@router.get("/sales-trend")
def sales_trend(
    current_user: User = Depends(require_active_subscription),
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
    current_user: User = Depends(require_active_subscription),
    db: Session = Depends(get_db)
):
    return {
        "status": "SUCCESS",
        "summary": get_revenue_expense_summary(
            db,
            current_user.tenant_id
        )
    }


@router.get("/financial-kpi")
def financial_kpi(
    current_user: User = Depends(require_active_subscription),
    db: Session = Depends(get_db)
):
    return {
        "status": "SUCCESS",
        "finance": get_financial_kpi_summary(
            db,
            current_user.tenant_id
        )
    }


@router.get("/finance-insight")
def finance_insight(
    current_user: User = Depends(require_active_subscription),
    db: Session = Depends(get_db)
):
    return {
        "status": "SUCCESS",
        "ai_finance": get_finance_insight(
            db,
            current_user.tenant_id
        )
    }



@router.get(
    "/owner/dashboard",
    response_class=HTMLResponse
)
def owner_dashboard(
    request: Request
):
    return templates.TemplateResponse(
        request=request,
        name="owner_dashboard.html",
        context={
            "request": request
        }
    )


@router.get("/platform-summary")
def owner_platform_summary(
    current_user: User = Depends(require_owner_role),
    db: Session = Depends(get_db)
):
    return {
        "status": "SUCCESS",
        "platform": get_owner_platform_summary(db)
    }



@router.get("/saas-revenue")
def saas_revenue(
    current_user: User = Depends(require_owner_role),
    db: Session = Depends(get_db)
):
    return {
        "status": "SUCCESS",
        "revenue": get_saas_revenue_summary(db)
    }


# ======================================
# OWNER RENEWAL CONTROL CENTER
# ======================================

@router.get("/renewals")
def owner_renewal_dashboard(

    db: Session = Depends(get_db)

):

    return get_owner_renewal_summary(
        db
    )



# ======================================
# SOCIAL CENTER DASHBOARD
# ======================================

@router.get("/social-summary")
def social_summary(
    current_user: User = Depends(require_active_subscription),
    db: Session = Depends(get_db)
):

    return {
        "status": "SUCCESS",
        "social": get_social_summary(
            db,
            current_user.tenant_id
        )
    }



# ======================================
# DASHBOARD WIDGETS
# ======================================

@router.get("/api/v4/dashboard/widgets")
async def dashboard_widgets(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    today = DashboardService.get_today_stats(
        db,
        current_user.tenant_id
    )

    chart = DashboardService.get_revenue_chart(
        db,
        current_user.tenant_id
    )

    return {
        "today": today,
        "sales_chart": chart
    }

