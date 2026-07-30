from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user
from src.models.saas_core import User

from src.security_center.service import SecurityCenterService
from src.security_center.schemas import SecurityOverviewResponse


router = APIRouter(
    prefix="/api/v4/security-center",
    tags=["Security Center"]
)


@router.get(
    "/overview",
    response_model=SecurityOverviewResponse
)
def security_center_overview(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return SecurityCenterService.get_overview(
        db=db,
        tenant_id=current_user.tenant_id
    )


@router.get(
    "/events"
)
def security_center_events(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return SecurityCenterService.get_events(
        db=db,
        tenant_id=current_user.tenant_id
    )




@router.get(
    "/devices"
)
def security_center_devices(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return {
        "devices": SecurityCenterService.get_devices(
            db=db,
            tenant_id=current_user.tenant_id
        )
    }

@router.get(
    "/sessions"
)
def security_center_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return {
        "sessions": SecurityCenterService.get_sessions(
            db=db,
            tenant_id=current_user.tenant_id
        )
    }

