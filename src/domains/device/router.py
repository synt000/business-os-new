from fastapi import APIRouter, Depends, HTTPException, Request
from datetime import timezone
from sqlalchemy.orm import Session
from sqlalchemy import func
import hashlib

from src.core.database import get_db
from src.core.security import get_current_user
from src.models.saas_core import User
from src.domains.device.models import TenantDevice
from src.security.event_logger import log_security_event
from src.domains.device.service import (
    list_device_sessions,
    block_device_session,
    unblock_device_session
)

from src.security.security_query import get_security_overview


router = APIRouter(
    prefix="/api/v4/security",
    tags=["Device Security"]
)


def generate_fingerprint(request: Request):

    raw = (
        request.headers.get("user-agent","")
        +
        request.client.host
    )

    return hashlib.sha256(
        raw.encode()
    ).hexdigest()


@router.post("/register")
def register_device(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    fingerprint = generate_fingerprint(request)


    existing = (
        db.query(TenantDevice)
        .filter(
            TenantDevice.user_id == current_user.id,
            TenantDevice.device_fingerprint == fingerprint
        )
        .first()
    )


    if existing:
        existing.last_seen = func.now()
        db.commit()

        return {
            "message":"DEVICE_ALREADY_REGISTERED",
            "device_id":existing.id
        }


    count = (
        db.query(TenantDevice)
        .filter(
            TenantDevice.user_id == current_user.id,
            TenantDevice.is_active == True
        )
        .count()
    )


    if count >= 1:
        raise HTTPException(
            status_code=403,
            detail="ONE_DEVICE_ONLY"
        )


    device = TenantDevice(
        tenant_id=current_user.tenant_id,
        user_id=current_user.id,
        device_fingerprint=fingerprint,
        device_name=request.headers.get("user-agent"),
        platform="WEB",
        browser=request.headers.get("user-agent")
    )


    db.add(device)
    db.commit()
    db.refresh(device)


    return {
        "message":"DEVICE_REGISTERED",
        "device_id":device.id
    }


# =====================================================
# Identity Security v5.8
# Device Session Management API
# =====================================================


@router.get("/overview")
def security_overview(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_security_overview(
        db,
        current_user.tenant_id
    )



@router.get(
    "/devices"
)
def get_security_devices(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    devices = list_device_sessions(
        db,
        current_user.tenant_id
    )

    return [
        {
            "id": d.id,
            "device_name": d.device_name,
            "platform": d.platform,
            "browser": d.browser,
            "screen_width": d.screen_width,
            "screen_height": d.screen_height,
            "timezone_name": d.timezone_name,
            "language": d.language,
            "last_seen": (d.last_seen.replace(tzinfo=timezone.utc) if d.last_seen and d.last_seen.tzinfo is None else d.last_seen),
            "is_blocked": d.is_blocked,
        }
        for d in devices
    ]


@router.post(
    "/devices/{device_id}/block"
)
def block_security_device(
    device_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    device = block_device_session(
        db,
        current_user.tenant_id,
        device_id
    )

    if not device:
        raise HTTPException(
            status_code=404,
            detail="DEVICE_NOT_FOUND"
        )

    return {
        "message": "DEVICE_BLOCKED",
        "device_id": device.id
    }



@router.post(
    "/devices/{device_id}/unblock"
)
def unblock_security_device(
    device_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    device = unblock_device_session(
        db,
        current_user.tenant_id,
        device_id
    )

    if not device:
        raise HTTPException(
            status_code=404,
            detail="DEVICE_NOT_FOUND"
        )




    return {
        "message": "DEVICE_UNBLOCKED",
        "device_id": device.id
    }
