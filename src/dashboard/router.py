import os

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user
from src.services.dashboard_service import DashboardService
from src.models.saas_core import User


router = APIRouter(
    tags=["Enterprise Dashboard"]
)


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


templates = Jinja2Templates(
    directory=os.path.join(
        BASE_DIR,
        "templates"
    )
)



@router.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )




@router.get("/social/ui", response_class=HTMLResponse)
async def social_center_ui(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="social_center.html"
    )


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )



@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html"
    )



@router.get(
    "/api/v4/dashboard/summary"
)
async def dashboard_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return DashboardService.get_summary(
        db,
        current_user.tenant_id
    )



@router.get("/products/ui", response_class=HTMLResponse)
async def products_ui(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="products.html"
    )



@router.get("/inventory/ui", response_class=HTMLResponse)
async def inventory_ui(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="inventory.html"
    )



@router.get("/orders/ui", response_class=HTMLResponse)
async def orders_ui(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="orders.html"
    )



@router.get("/customers/ui", response_class=HTMLResponse)
async def customers_ui(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="customers.html"
    )



@router.get("/suppliers/ui", response_class=HTMLResponse)
async def suppliers_ui(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="suppliers.html"
    )


@router.get("/customers/ui", response_class=HTMLResponse)
async def customers_ui(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="customers.html"
    )


@router.get("/suppliers/ui", response_class=HTMLResponse)
async def suppliers_ui(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="suppliers.html"
    )


@router.get("/customers/ui", response_class=HTMLResponse)
async def customers_ui(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="customers.html"
    )


@router.get("/suppliers/ui", response_class=HTMLResponse)
async def suppliers_ui(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="suppliers.html"
    )



@router.get("/api/public/home-summary")
async def public_home_summary(
    db: Session = Depends(get_db)
):

    from sqlalchemy import func
    from src.models.saas_core import Tenant, Order, AccountLedger
    from src.domains.product.models import Product


    tenant = (
        db.query(Tenant)
        .order_by(Tenant.created_at.asc())
        .first()
    )


    if not tenant:
        return {
            "revenue": 0,
            "orders": 0,
            "products": 0,
            "subscription": "NONE"
        }


    revenue = (
        db.query(func.sum(AccountLedger.amount))
        .filter(
            AccountLedger.tenant_id == tenant.id,
            AccountLedger.entry_type == "CREDIT"
        )
        .scalar()
        or 0
    )


    orders = (
        db.query(Order)
        .filter(
            Order.tenant_id == tenant.id
        )
        .count()
    )


    products = (
        db.query(Product)
        .filter(
            Product.tenant_id == tenant.id
        )
        .count()
    )


    return {
        "revenue": revenue,
        "orders": orders,
        "products": products,
        "subscription": tenant.subscription_tier.value
    }





@router.get("/api/v4/dashboard/today-stats")
async def today_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return DashboardService.get_today_stats(
        db,
        current_user.tenant_id
    )


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


@router.get("/api/v4/dashboard/revenue-chart")
async def revenue_chart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return DashboardService.get_revenue_chart(
        db,
        current_user.tenant_id
    )
