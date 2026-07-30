from sqlalchemy.orm import Session

from src.security.security_query import get_security_overview, get_security_risk_summary
from src.models.security_event import SecurityEvent
from src.models.login_session import LoginSession


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


from src.domains.device.service import (
    list_device_sessions,
    block_device_session,
    trust_device_session
)




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

class _SecurityCenterSessionsMixin:

    @staticmethod
    def get_sessions(
        db: Session,
        tenant_id: str
    ):
        sessions = (
            db.query(LoginSession)
            .filter(
                LoginSession.tenant_id == tenant_id
            )
            .order_by(
                LoginSession.login_at.desc()
            )
            .limit(50)
            .all()
        )

        return [
            {
                "id": s.id,
                "device_name": s.device_name,
                "ip_address": s.ip_address,
                "risk_level": s.risk_level,
                "risk_score": s.risk_score,
                "login_type": s.login_type,
                "is_new_device": s.is_new_device,
                "login_at": (
                    s.login_at.isoformat()
                    if s.login_at
                    else None
                ),
                "last_seen": (
                    s.last_seen.isoformat()
                    if s.last_seen
                    else None
                ),
                "is_active": s.is_active,
            }
            for s in sessions
        ]


SecurityCenterService.get_sessions = staticmethod(
    _SecurityCenterSessionsMixin.get_sessions
)



RISK_WEIGHTS = {
    "new_device": 5,
    "blocked_device": 10,
    "medium_risk": 15,
    "high_risk": 30,
}


def calculate_risk_score(metrics):
    return (
        metrics.get("new_devices", 0)
        * RISK_WEIGHTS["new_device"]
        +
        metrics.get("blocked_devices", 0)
        * RISK_WEIGHTS["blocked_device"]
        +
        metrics.get("medium_risk", 0)
        * RISK_WEIGHTS["medium_risk"]
        +
        metrics.get("high_risk", 0)
        * RISK_WEIGHTS["high_risk"]
    )


def resolve_risk_level(score):
    if score <= 24:
        return "LOW"

    if score <= 49:
        return "MEDIUM"

    return "HIGH"


def build_recommendations(metrics):
    recommendations = []

    if metrics.get("high_risk", 0) > 0:
        recommendations.append(
            "Investigate high-risk login activity immediately."
        )

    if metrics.get("blocked_devices", 0) > 5:
        recommendations.append(
            "Review blocked devices for unusual patterns."
        )

    if metrics.get("new_devices", 0) > 3:
        recommendations.append(
            "Verify newly registered devices."
        )

    if not recommendations:
        recommendations.append(
            "No immediate security action required."
        )

    return recommendations


def _security_center_get_risk(
    db: Session,
    tenant_id: str
):
    metrics = get_security_risk_summary(
        db=db,
        tenant_id=tenant_id
    )

    score = calculate_risk_score(metrics)

    return {
        "risk_level": resolve_risk_level(score),
        "risk_score": score,
        "today_logins": metrics.get("today_logins", 0),
        "failed_logins": 0,
        "new_devices": metrics.get("new_devices", 0),
        "blocked_devices": metrics.get("blocked_devices", 0),
        "medium_risk": metrics.get("medium_risk", 0),
        "high_risk": metrics.get("high_risk", 0),
        "recommendations": build_recommendations(metrics),
    }


SecurityCenterService.get_risk = staticmethod(
    _security_center_get_risk
)


RISK_WEIGHTS = {
    "new_device": 5,
    "blocked_device": 10,
    "medium_risk": 15,
    "high_risk": 30,
}


def calculate_risk_score(metrics: dict) -> int:
    return (
        metrics.get("new_devices", 0)
        * RISK_WEIGHTS["new_device"]
        +
        metrics.get("blocked_devices", 0)
        * RISK_WEIGHTS["blocked_device"]
        +
        metrics.get("medium_risk", 0)
        * RISK_WEIGHTS["medium_risk"]
        +
        metrics.get("high_risk", 0)
        * RISK_WEIGHTS["high_risk"]
    )


def resolve_risk_level(score: int) -> str:

    if score <= 24:
        return "LOW"

    if score <= 49:
        return "MEDIUM"

    return "HIGH"


def _build_recommendations(metrics: dict):

    recommendations = []

    if metrics.get("high_risk", 0) > 0:
        recommendations.append(
            "Investigate high-risk login activity immediately."
        )

    if metrics.get("blocked_devices", 0) > 5:
        recommendations.append(
            "Review blocked devices for unusual patterns."
        )

    if metrics.get("new_devices", 0) > 3:
        recommendations.append(
            "Verify newly registered devices."
        )

    if not recommendations:
        recommendations.append(
            "No immediate security action required."
        )

    return recommendations


SecurityCenterService.calculate_risk_score = staticmethod(
    calculate_risk_score
)

SecurityCenterService.resolve_risk_level = staticmethod(
    resolve_risk_level
)

SecurityCenterService.build_recommendations = staticmethod(
    _build_recommendations
)


@staticmethod
def _get_risk(
    db: Session,
    tenant_id: str
):

    metrics = get_security_risk_summary(
        db=db,
        tenant_id=tenant_id
    )

    score = calculate_risk_score(metrics)

    return {
        "risk_level": resolve_risk_level(score),
        "risk_score": score,
        "today_logins": metrics.get("today_logins", 0),
        "failed_logins": 0,
        "new_devices": metrics.get("new_devices", 0),
        "blocked_devices": metrics.get("blocked_devices", 0),
        "medium_risk": metrics.get("medium_risk", 0),
        "high_risk": metrics.get("high_risk", 0),
        "recommendations": _build_recommendations(metrics),
    }


SecurityCenterService.get_risk = staticmethod(_get_risk)


# =====================================================
# Phase 5.9.6
# Device Management Wrappers
# =====================================================

@staticmethod
def _block_device(
    db: Session,
    tenant_id: str,
    device_id: str,
):
    return block_device_session(
        db=db,
        tenant_id=tenant_id,
        device_id=device_id,
    )


@staticmethod
def _trust_device(
    db: Session,
    tenant_id: str,
    device_id: str,
):
    return trust_device_session(
        db=db,
        tenant_id=tenant_id,
        device_id=device_id,
    )


SecurityCenterService.block_device = staticmethod(_block_device)
SecurityCenterService.trust_device = staticmethod(_trust_device)

