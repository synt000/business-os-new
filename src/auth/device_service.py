from datetime import datetime, timezone

from sqlalchemy.orm import Session

from src.models.device_session import DeviceSession


def get_device(
    db: Session,
    *,
    workspace_id: str,
    fingerprint: str,
):

    return (
        db.query(DeviceSession)
        .filter(
            DeviceSession.device_fingerprint == fingerprint,
            DeviceSession.workspace_id == workspace_id,
        )
        .first()
    )


def register_device(
    db: Session,
    *,
    workspace_id: str,
    device_fingerprint: str,
    device_name: str | None = None,
    platform: str | None = None,
    browser: str | None = None,
    screen_width: str | None = None,
    screen_height: str | None = None,
    timezone_name: str | None = None,
    language: str | None = None,
    ip_address: str | None = None,
    user_agent: str | None = None,
):

    existing = get_device(
        db,
        workspace_id=workspace_id,
        fingerprint=device_fingerprint,
    )


    if existing:

        if existing.is_blocked:
            return existing, False

        existing.last_seen = datetime.now(
            timezone.utc
        )

        existing.ip_address = ip_address
        existing.user_agent = user_agent

        db.commit()
        db.refresh(existing)

        return existing, False


    device = DeviceSession(

        workspace_id=workspace_id,

        device_fingerprint=device_fingerprint,

        device_name=device_name,

        platform=platform,

        browser=browser,

        screen_width=screen_width,

        screen_height=screen_height,

        timezone_name=timezone_name,

        language=language,

        ip_address=ip_address,

        user_agent=user_agent,

    )


    db.add(device)

    db.commit()

    db.refresh(device)


    return device, True



def block_device(
    db: Session,
    *,
    workspace_id: str,
    fingerprint: str,
):

    device = get_device(
        db,
        workspace_id=workspace_id,
        fingerprint=fingerprint,
    )


    if not device:
        return False


    device.is_blocked = True

    db.commit()

    return True
