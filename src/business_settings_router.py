from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user
from src.models.business_profile import BusinessProfile
from src.models.saas_core import User


router = APIRouter(
    prefix="/api/v4/business",
    tags=["Business Settings"]
)


@router.put("/settings")
async def update_business_settings(
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    profile = (
        db.query(BusinessProfile)
        .filter(
            BusinessProfile.tenant_id == current_user.tenant_id
        )
        .first()
    )

    if not profile:
        return {
            "status": "PROFILE_NOT_FOUND"
        }


    allowed_fields = [
        "business_name",
        "owner_name",
        "phone",
        "owner_phone",
        "email",
        "address",
        "facebook_username",
        "telegram_username",
        "viber_number",
        "website_url",
        "welcome_message",
        "description",
        "theme_color"
    ]


    for field in allowed_fields:
        if field in data:
            setattr(
                profile,
                field,
                data[field]
            )


    db.commit()
    db.refresh(profile)


    return {
        "status": "UPDATED",
        "business_name": profile.business_name,
        "owner_name": profile.owner_name,
        "phone": profile.owner_phone,
        "telegram": profile.telegram_username,
        "facebook": profile.facebook_username,
        "viber": profile.viber_number
    }
