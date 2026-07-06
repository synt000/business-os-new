from sqlalchemy.orm import Session
from domains.audit.model import AuditLog
from uuid import UUID

class AuditRepository:
    @staticmethod
    def log_action(db: Session, tenant_id: UUID, user_id: str, action: str, resource_id: str = None):
        log = AuditLog(
            tenant_id=tenant_id,
            user_id=user_id,
            action=action,
            resource_id=resource_id
        )
        db.add(log)
        db.commit()
