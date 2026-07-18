from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.models.business_profile import BusinessProfile

BLOCKED_PUBLIC_PATHS = {
    "favicon.ico",
    "dashboard",
    "login",
    "logout",
    "api",
    "docs",
    "openapi.json"
}

router = APIRouter(
    prefix="",
    tags=["Public Web Page"]
)

templates = Jinja2Templates(directory="src/templates")


@router.get("/", response_class=HTMLResponse)
async def read_landing_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="owner_dashboard.html",
        context={}
    )


@router.get("/landing-page", response_class=HTMLResponse)
async def read_test_landing_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="owner_dashboard.html"
    )


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
        name="landing.html",
        context={
            "business": profile
        }
    )
