from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.models.business_profile import BusinessProfile


router = APIRouter(
    prefix="/api/v4/public",
    tags=["Public Homepage"]
)


@router.get("/{business_slug}")
async def get_public_business_homepage(
    business_slug: str,
    db: Session = Depends(get_db)
):

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
            detail="BUSINESS_PUBLIC_PAGE_NOT_FOUND"
        )

    return {
        "business_name": profile.business_name,
        "welcome_message": profile.welcome_message,
        "description": profile.description,
        "logo_url": profile.logo_url,
        "cover_url": profile.cover_url,
        "phone": profile.phone,
        "address": profile.address,
        "qr_code": profile.qr_code,
        "theme_color": profile.theme_color,
        "start_button": True
    }
