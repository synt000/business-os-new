from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
import hashlib

from src.core.database import get_db
from src.core.security import get_current_user
from src.models.saas_core import User
from src.domains.device.models import TenantDevice


router = APIRouter(
    prefix="/devices",
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
