from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.models.business_profile import BusinessProfile


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
    request: Request
):
    return templates.TemplateResponse(
        request=request,
        name="welcome.html"
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
# PUBLIC BUSINESS PAGE
# ================================
@router.get("/{business_slug}", response_class=HTMLResponse)
async def public_business_page(
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


    return templates.TemplateResponse(
        request=None,
        name="business.html",
        context={
            "business": profile
        }
    )
