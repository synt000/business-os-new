from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from src.core.database import get_db
from src.domains.license.models import LicenseKey, LicenseDevice, LicenseEvent
from src.domains.license.schemas import (
    LicenseCreate,
    LicenseActivate
)

import secrets


router = APIRouter(
    prefix="/api/v4/license",
    tags=["License Management"]
)


@router.post("/create")
def create_license(
    payload: LicenseCreate,
    db: Session = Depends(get_db)
):

    key = "BOS-" + secrets.token_hex(8).upper()

    license_obj = LicenseKey(
        tenant_id=payload.tenant_id,
        key=key,
        max_devices=payload.max_devices,
        expires_at=payload.expires_at
    )

    db.add(license_obj)
    db.commit()
    db.refresh(license_obj)

    return {
        "status":"LICENSE_CREATED",
        "license_key":license_obj.key
    }


@router.post("/activate")
def activate_license(
    payload: LicenseActivate,
    db: Session = Depends(get_db)
):

    license_obj = (
        db.query(LicenseKey)
        .filter(
            LicenseKey.key == payload.license_key
        )
        .first()
    )

    if not license_obj:
        raise HTTPException(
            status_code=404,
            detail="LICENSE_NOT_FOUND"
        )


    if not license_obj.is_active:
        raise HTTPException(
            status_code=403,
            detail="LICENSE_DISABLED"
        )


    device_count = (
        db.query(LicenseDevice)
        .filter(
            LicenseDevice.license_id == license_obj.id
        )
        .count()
    )


    if device_count >= license_obj.max_devices:
        raise HTTPException(
            status_code=403,
            detail="DEVICE_LIMIT_REACHED"
        )


    device = LicenseDevice(
        license_id=license_obj.id,
        hardware_uid=payload.hardware_uid,
        device_name=payload.device_name,
        client_ip=payload.client_ip
    )


    db.add(device)


    event = LicenseEvent(
        license_id=license_obj.id,
        event_type="DEVICE_ACTIVATED"
    )

    db.add(event)

    db.commit()


    return {
        "status":"ACTIVATED",
        "license":license_obj.key
    }


@router.get("/validate/{license_key}")
def validate_license(
    license_key:str,
    db:Session=Depends(get_db)
):

    obj = (
        db.query(LicenseKey)
        .filter(
            LicenseKey.key == license_key
        )
        .first()
    )


    if not obj:
        return {
            "valid":False
        }


    return {
        "valid":obj.is_active,
        "expires_at":obj.expires_at
    }
