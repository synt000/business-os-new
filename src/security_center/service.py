from sqlalchemy.orm import Session

from src.security.security_query import get_security_overview


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
