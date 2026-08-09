from datetime import datetime
from .service import get_ai_decision_engine, get_ai_growth_plan, get_smart_restock, get_sales_forecast, get_ceo_report, get_top_product_intelligence, get_customer_intelligence, get_ai_dashboard
from src.domains.dashboard.services.cashflow_service import get_cashflow_dashboard
from src.domains.dashboard.services.seller_analytics_service import get_revenue_summary, get_daily_revenue, get_order_summary, get_daily_order_summary, get_customer_count

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


@router.get("/seller/revenue")
def seller_revenue_analytics(
    current_user: User = Depends(require_active_subscription),
    db: Session = Depends(get_db),
):
    now = datetime.utcnow()

    start_at = datetime(now.year, now.month, now.day)

    summary = get_revenue_summary(
        db=db,
        tenant_id=current_user.tenant_id,
        start_at=start_at,
        end_at=now,
    )

    daily_revenue = get_daily_revenue(
        db=db,
        tenant_id=current_user.tenant_id,
        start_at=start_at,
        end_at=now,
    )

    return {
        "status": "SUCCESS",
        **summary,
        "daily_revenue": daily_revenue,
    }


@router.get("/seller/orders")
def seller_order_analytics(
    current_user: User = Depends(require_active_subscription),
    db: Session = Depends(get_db),
):
    now = datetime.utcnow()
    start_at = datetime(now.year, now.month, now.day)

    summary = get_order_summary(
        db=db,
        tenant_id=current_user.tenant_id,
        start_at=start_at,
        end_at=now,
    )

    daily_orders = get_daily_order_summary(
        db=db,
        tenant_id=current_user.tenant_id,
        start_at=start_at,
        end_at=now,
    )

    customer_count = get_customer_count(
        db=db,
        tenant_id=current_user.tenant_id,
        start_at=start_at,
        end_at=now,
    )

    return {
        "status": "SUCCESS",
        **summary,
        "customer_count": customer_count,
        "daily_orders": daily_orders,
    }


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
    "/dashboard",
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
    current_user: User = Depends(require_owner_role),
    db: Session = Depends(get_db)
):
    return get_owner_renewal_summary(
        db,
        current_user.tenant_id
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



# ======================================
# AI DECISION ENGINE API v8
# ======================================

@router.get("/ai-decision")
def ai_decision(
    current_user: User = Depends(require_active_subscription),
    db: Session = Depends(get_db)
):

    return {
        "status": "SUCCESS",
        "ai_decision": get_ai_decision_engine(
            db,
            current_user.tenant_id
        )
    }



# ======================================
# AI GROWTH PLAN API
# ======================================

@router.get("/growth-plan")
def growth_plan(

    current_user: User = Depends(require_active_subscription),

    db: Session = Depends(get_db)

):

    return {

        "status":"SUCCESS",

        "growth_plan":
        get_ai_growth_plan(
            db,
            current_user.tenant_id
        )

    }




# ======================================
# SMART RESTOCK API
# ======================================

@router.get("/smart-restock")
def smart_restock(

    current_user: User = Depends(require_active_subscription),

    db: Session = Depends(get_db)

):

    return {

        "status":"SUCCESS",

        "smart_restock":
        get_smart_restock(
            db,
            current_user.tenant_id
        )

    }




# ======================================
# CEO REPORT API
# ======================================

@router.get("/ceo-report")
def ceo_report(

    current_user: User = Depends(require_active_subscription),

    db: Session = Depends(get_db)

):

    return {

        "status":"SUCCESS",

        "ceo_report":
        get_ceo_report(
            db,
            current_user.tenant_id
        )

    }




# ======================================
# AI SALES FORECAST API
# ======================================

@router.get("/sales-forecast")
def sales_forecast(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return {
        "status": "SUCCESS",
        "sales_forecast": get_sales_forecast(
            db,
            current_user.tenant_id
        )
    }



# ======================================
# AI TOP PRODUCT API
# ======================================

@router.get("/top-products")
def top_products(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return {
        "status": "SUCCESS",
        "top_product": get_top_product_intelligence(
            db,
            current_user.tenant_id
        )
    }


# ======================================
# ======================================
# AI CUSTOMER INTELLIGENCE API
# ======================================

@router.get("/customer-intelligence")
def customer_intelligence(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return {

        "status":
        "SUCCESS",

        "customer_intelligence":
        get_customer_intelligence(
            db,
            current_user.tenant_id
        )

    }

# ======================================
# AI EXECUTIVE DASHBOARD API
# ======================================

@router.get("/ai-dashboard")
def ai_dashboard(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    dashboard = get_ai_dashboard(
        db,
        current_user.tenant_id
    )


    return {
        "status": "SUCCESS",
        "executive_dashboard": dashboard
    }


@router.get("/cashflow")
def cashflow_dashboard(
    db=Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_cashflow_dashboard(
        db,
        current_user.tenant_id
    )
