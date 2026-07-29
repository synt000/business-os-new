from datetime import datetime, timezone
import uuid

from sqlalchemy.orm import Session

from src.domains.device.models import TenantDevice
from src.models.device_session import DeviceSession
from src.security.event_logger import log_security_event


MAX_DEVICES_PER_USER = 1


def check_device_limit(
    db: Session,
    tenant_id: str,
    user_id: str
):
    count = (
        db.query(TenantDevice)
        .filter(
            TenantDevice.tenant_id == tenant_id,
            TenantDevice.user_id == user_id,
            TenantDevice.is_active == True
        )
        .count()
    )

    return count < MAX_DEVICES_PER_USER


def register_device(
    db: Session,
    tenant_id: str,
    user_id: str,
    device_fingerprint: str,
    device_name: str = None,
    platform: str = None,
    browser: str = None
):

    existing = (
        db.query(TenantDevice)
        .filter(
            TenantDevice.tenant_id == tenant_id,
            TenantDevice.user_id == user_id,
            TenantDevice.device_fingerprint == device_fingerprint
        )
        .first()
    )

    if existing:
        existing.last_seen = datetime.now(timezone.utc)
        existing.is_active = True

        db.commit()
        db.refresh(existing)

        return existing


    if not check_device_limit(
        db,
        tenant_id,
        user_id
    ):
        raise Exception(
            "DEVICE_LIMIT_REACHED"
        )


    device = TenantDevice(
        id=str(uuid.uuid4()),
        tenant_id=tenant_id,
        user_id=user_id,
        device_fingerprint=device_fingerprint,
        device_name=device_name,
        platform=platform,
        browser=browser,
        is_active=True
    )


    db.add(device)
    db.commit()
    db.refresh(device)

    return device



def deactivate_device(
    db: Session,
    device_id: str
):

    device = (
        db.query(TenantDevice)
        .filter(
            TenantDevice.id == device_id
        )
        .first()
    )

    if not device:
        return False


    device.is_active = False

    db.commit()

    return True


# =====================================================
# Identity Security v5.8
# DeviceSession Management
# =====================================================


def list_device_sessions(
    db: Session,
    tenant_id: str
):
    return (
        db.query(DeviceSession)
        .filter(
            DeviceSession.workspace_id == tenant_id
        )
        .order_by(
            DeviceSession.id.desc()
        )
        .all()
    )


def block_device_session(
    db: Session,
    tenant_id: str,
    device_id: str
):
    device = (
        db.query(DeviceSession)
        .filter(
            DeviceSession.id == device_id,
            DeviceSession.workspace_id == tenant_id
        )
        .first()
    )

    if not device:
        return None

    device.is_blocked = True

    log_security_event(
        db,
        event_type="DEVICE_BLOCKED_BY_ADMIN",
        user_id=None,
        tenant_id=tenant_id,
        device_info={
            "device_id": device.id,
            "fingerprint": device.device_fingerprint,
            "browser": device.browser,
            "platform": device.platform,
        },
        description="Device blocked by administrator"
    )

    db.commit()
    db.refresh(device)

    return device


def unblock_device_session(
    db: Session,
    tenant_id: str,
    device_id: str
):
    device = (
        db.query(DeviceSession)
        .filter(
            DeviceSession.id == device_id,
            DeviceSession.workspace_id == tenant_id
        )
        .first()
    )

    if not device:
        return None

    device.is_blocked = False

    db.commit()
    db.refresh(device)

    return device
