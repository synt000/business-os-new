import uuid
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from src.models.guest_workspace import GuestWorkspace
from src.models.device_session import DeviceSession


class GuestWorkspaceService:


    @staticmethod
    def create_workspace(
        db: Session,
        device_data,
        guest_name="Guest",
        business_type_id=None
    ):

        # Existing device protection
        existing_device = (
            db.query(DeviceSession)
            .filter(
                DeviceSession.device_fingerprint ==
                device_data.device_fingerprint
            )
            .first()
        )

        if existing_device:
            existing_workspace = (
                db.query(GuestWorkspace)
                .filter(
                    GuestWorkspace.id ==
                    existing_device.workspace_id
                )
                .first()
            )

            if existing_workspace:
                existing_workspace.last_seen_at = datetime.utcnow()
                db.commit()
                db.refresh(existing_workspace)
                return existing_workspace

        workspace = GuestWorkspace(
            id=str(uuid.uuid4()),
            workspace_key=str(uuid.uuid4()),
            device_id=device_data.device_fingerprint,
            guest_name=guest_name,
            business_type_id=business_type_id,
            created_at=datetime.utcnow(),
            last_seen_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(days=7),
            is_active=True
        )

        db.add(workspace)
        db.flush()


        device = DeviceSession(
            id=str(uuid.uuid4()),
            workspace_id=workspace.id,
            device_fingerprint=device_data.device_fingerprint,
            device_name=device_data.device_name,
            platform=device_data.platform,
            browser=device_data.browser,
            screen_width=device_data.screen_width,
            screen_height=device_data.screen_height,
            timezone=device_data.timezone,
            language=device_data.language,
            ip_address=device_data.ip_address,
            user_agent=device_data.user_agent,
            first_seen=datetime.utcnow(),
            last_seen=datetime.utcnow(),
            is_blocked=False
        )

        db.add(device)
        db.commit()
        db.refresh(workspace)

        return workspace


    @staticmethod
    def get_workspace_info(
        db: Session,
        workspace_key: str
    ):

        workspace = (
            db.query(GuestWorkspace)
            .filter(
                GuestWorkspace.workspace_key == workspace_key
            )
            .first()
        )

        if not workspace:
            return None

        return {
            "workspace_key": workspace.workspace_key,
            "guest_name": workspace.guest_name,
            "mode": "DEMO",
            "expires_at": workspace.expires_at,
            "is_active": workspace.is_active,
            "modules": [
                "POS",
                "Inventory",
                "Sales",
                "Reports"
            ],
            "require_signup": True
        }
