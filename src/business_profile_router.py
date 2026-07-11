from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user

from src.models.business_profile import BusinessProfile
from src.schemas.business_profile import (
    BusinessProfileCreate,
    BusinessProfileResponse
)

from src.models.saas_core import User


router = APIRouter(
    prefix="/api/v4/business",
    tags=["Business Profile"]
)


@router.post(
    "/profile",
    response_model=BusinessProfileResponse
)
async def create_or_update_profile(
    payload: BusinessProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    profile = db.query(BusinessProfile).filter(
        BusinessProfile.tenant_id == current_user.tenant_id
    ).first()


    if profile:
        for key, value in payload.dict().items():
            setattr(profile, key, value)

    else:
        profile = BusinessProfile(
            tenant_id=current_user.tenant_id,
            **payload.dict()
        )

        db.add(profile)


    db.commit()
    db.refresh(profile)

    return profile



@router.get(
    "/profile",
    response_model=BusinessProfileResponse
)
async def get_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return db.query(BusinessProfile).filter(
        BusinessProfile.tenant_id == current_user.tenant_id
    ).first()
