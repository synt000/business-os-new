from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.models.business_profile import BusinessProfile
from src.domains.product.models import Product
from src.domains.welcome.service import WelcomeService


BLOCKED_PUBLIC_PATHS = {
    "favicon.ico",

    # frontend/system
    "dashboard",
    "login",
    "logout",

    # api/system
    "api",
    "docs",
    "openapi.json",

    # business modules
    "products",
    "orders",
    "customers",
    "suppliers",
    "inventory",
    "payments",
    "invoices",
    "accounting",

    # dashboard api
    "business-health",
    "ceo-summary",
    "financial-kpi",
    "finance-insight",
    "executive-ai",
    "menus",

    # owner
    "owner"
}


router = APIRouter(
    prefix="",
    tags=["Public Web Page"]
)


templates = Jinja2Templates(
    directory="src/templates"
)




# ================================
# WELCOME PAGE
# ================================
@router.get("/welcome", response_class=HTMLResponse)
async def welcome_page(
    request: Request,
    db: Session = Depends(get_db)
):

    welcome = WelcomeService.get_welcome(
        db,
        "mm"
    )

    return templates.TemplateResponse(
        request=request,
        name="welcome.html",
        context={
            "welcome": welcome
        }
    )



# ================================
# CHOOSE BUSINESS TYPE
# ================================

@router.get("/choose-business", response_class=HTMLResponse)
async def choose_business_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="choose_business.html"
    )

# ================================
# MAIN HOMEPAGE
# ================================
@router.get("/", response_class=HTMLResponse)
async def read_landing_page(
    request: Request,
    db: Session = Depends(get_db)
):

    businesses = (
        db.query(BusinessProfile)
        .filter(
            BusinessProfile.is_public == True
        )
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="landing.html",
        context={
            "businesses": businesses
        }
    )


# ================================
# TEST LANDING PAGE
# ================================
@router.get("/landing-page", response_class=HTMLResponse)
async def read_test_landing_page(
    request: Request,
    db: Session = Depends(get_db)
):

    businesses = (
        db.query(BusinessProfile)
        .filter(
            BusinessProfile.is_public == True
        )
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="landing.html",
        context={
            "businesses": businesses
        }
    )




# ================================
# SIGNUP PAGE
# ================================

@router.get("/signup", response_class=HTMLResponse)
async def signup_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="signup.html"
    )

# ================================
# PUBLIC BUSINESS PAGE
# ================================
@router.get("/shop/{business_slug}", response_class=HTMLResponse)
async def public_business_page(
    request: Request,
    business_slug: str,
    db: Session = Depends(get_db)
):

    if business_slug in BLOCKED_PUBLIC_PATHS:
        raise HTTPException(
            status_code=404,
            detail="PUBLIC_PAGE_NOT_FOUND"
        )


    profile = (
        db.query(BusinessProfile)
        .filter(
            BusinessProfile.business_slug == business_slug,
            BusinessProfile.is_public == True
        )
        .first()
    )


    if not profile:
        raise HTTPException(
            status_code=404,
            detail="BUSINESS_NOT_FOUND"
        )


    products = (
        db.query(Product)
        .filter(
            Product.tenant_id == profile.tenant_id
        )
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="business.html",
        context={
            "business": profile,
            "products": products
        }
    )


# ================================
# PUBLIC HOME HEALTH
# ================================

@router.get("/api/public/home-health")
async def public_home_health(
    db: Session = Depends(get_db)
):

    from sqlalchemy import text
    from src.models.saas_core import Tenant

    health = {
        "database": "Healthy",
        "accounting": "Balanced",
        "subscription": "Active",
        "security": "Protected"
    }

    try:
        db.execute(text("SELECT 1"))
        health["database"] = "Healthy"
    except Exception:
        health["database"] = "Error"

    tenant = db.query(Tenant).first()

    if tenant:
        if tenant.is_billing_active:
            health["subscription"] = "Active"
        else:
            health["subscription"] = "Inactive"

    return health


@router.get("/api/public/home-revenue-chart")
async def public_home_revenue_chart(
    db: Session = Depends(get_db)
):
    from sqlalchemy import func
    from src.domains.accounting.models import AccountLedger

    rows = (
        db.query(
            func.date(AccountLedger.created_at),
            func.sum(AccountLedger.amount)
        )
        .filter(
            AccountLedger.entry_type == "CREDIT"
        )
        .group_by(
            func.date(AccountLedger.created_at)
        )
        .order_by(
            func.date(AccountLedger.created_at)
        )
        .all()
    )

    return {
        "labels": [str(r[0]) for r in rows],
        "values": [float(r[1] or 0) for r in rows]
    }


@router.get("/api/public/home-activity")
async def public_home_activity(
    db: Session = Depends(get_db)
):
    from src.domains.accounting.models import AccountLedger
    from src.models.saas_core import Order

    activities = []

    payments = (
        db.query(AccountLedger)
        .order_by(AccountLedger.created_at.desc())
        .limit(5)
        .all()
    )

    for item in payments:
        activities.append({
            "title": item.account_head,
            "detail": f"{item.amount} MMK",
            "type": item.entry_type
        })

    orders = (
        db.query(Order)
        .order_by(Order.created_at.desc())
        .limit(3)
        .all()
    )

    for order in orders:
        activities.append({
            "title": "Order Created",
            "detail": order.order_number,
            "type": "ORDER"
        })

    return activities[:5]

