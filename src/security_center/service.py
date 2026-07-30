from sqlalchemy.orm import Session

from src.security.security_query import get_security_overview
from src.models.security_event import SecurityEvent


class SecurityCenterService:

    @staticmethod
    def get_overview(
        db: Session,
        tenant_id: str
    ):
        data = get_security_overview(
            db=db,
            tenant_id=tenant_id
        )

        return {
            "security_status": "SECURE",
            "today_new_devices": data.get(
                "today_new_devices",
                0
            ),
            "medium_risk_logins": data.get(
                "medium_risk_logins",
                0
            ),
            "high_risk_logins": data.get(
                "high_risk_logins",
                0
            ),
            "blocked_devices": data.get(
                "blocked_devices",
                0
            ),
            "latest_events": data.get(
                "latest_events",
                []
            )
        }

    @staticmethod
    def get_events(
        db: Session,
        tenant_id: str
    ):
        events = (
            db.query(SecurityEvent)
            .filter(
                SecurityEvent.tenant_id == tenant_id
            )
            .order_by(
                SecurityEvent.created_at.desc()
            )
            .limit(50)
            .all()
        )

        return [
            {
                "event": event.event_type,
                "risk": event.risk_level,
                "score": event.risk_score,
                "login_session_id": event.login_session_id,
                "device_session_id": event.device_session_id,
                "time": (
                    event.created_at.isoformat()
                    if event.created_at
                    else None
                )
            }
            for event in events
        ]


from src.domains.device.service import list_device_sessions




class _SecurityCenterDevicesMixin:

    @staticmethod
    def get_devices(
        db: Session,
        tenant_id: str
    ):
        devices = list_device_sessions(
            db=db,
            tenant_id=tenant_id
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
                "last_seen": (
                    d.last_seen.isoformat()
                    if d.last_seen
                    else None
                ),
                "is_blocked": d.is_blocked,
            }
            for d in devices
        ]


SecurityCenterService.get_devices = staticmethod(
    _SecurityCenterDevicesMixin.get_devices
)
