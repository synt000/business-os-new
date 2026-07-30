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



@router.get(
    "/risk"
)
def security_center_risk(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return SecurityCenterService.get_risk(
        db=db,
        tenant_id=current_user.tenant_id
    )

@router.post(
    "/devices/{device_id}/block"
)
def security_center_block_device(
    device_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    device = SecurityCenterService.block_device(
        db=db,
        tenant_id=current_user.tenant_id,
        device_id=device_id,
    )

    return {
        "success": device is not None,
        "device_id": device_id,
        "status": "BLOCKED" if device else "NOT_FOUND",
        "event": "DEVICE_BLOCKED_BY_ADMIN" if device else None,
    }


@router.post(
    "/devices/{device_id}/trust"
)
def security_center_trust_device(
    device_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    device = SecurityCenterService.trust_device(
        db=db,
        tenant_id=current_user.tenant_id,
        device_id=device_id,
    )

    return {
        "success": device is not None,
        "device_id": device_id,
        "status": "TRUSTED" if device else "NOT_FOUND",
        "event": "DEVICE_TRUSTED" if device else None,
    }

