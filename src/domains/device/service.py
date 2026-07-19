cat > src/domains/device/service.py <<'PY'
from datetime import datetime
import uuid

from sqlalchemy.orm import Session

from src.domains.device.models import TenantDevice


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
        existing.last_seen = datetime.utcnow()
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
