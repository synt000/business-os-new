from sqlalchemy.orm import Session

from src.domains.audit.models import AuditLog


class AuditService:

    @staticmethod
    def get_audit_logs(
        db: Session,
        tenant_id: str,
        page: int = 1,
        limit: int = 20,
        action: str | None = None,
        table_name: str | None = None,
        user_id: str | None = None,
    ):
        query = (
            db.query(AuditLog)
            .filter(
                AuditLog.tenant_id == tenant_id
            )
        )

        if action:
            query = query.filter(
                AuditLog.action == action
            )

        if table_name:
            query = query.filter(
                AuditLog.table_name == table_name
            )

        if user_id:
            query = query.filter(
                AuditLog.user_id == user_id
            )

        total = query.count()

        logs = (
            query
            .order_by(
                AuditLog.created_at.desc()
            )
            .offset(
                (page - 1) * limit
            )
            .limit(limit)
            .all()
        )

        return {
            "items": [
                {
                    "id": log.id,
                    "action": log.action,
                    "table_name": log.table_name,
                    "record_id": log.record_id,
                    "changes": log.changes,
                    "user_id": log.user_id,
                    "created_at": (
                        log.created_at.isoformat()
                        if log.created_at
                        else None
                    ),
                    "updated_at": (
                        log.updated_at.isoformat()
                        if log.updated_at
                        else None
                    ),
                }
                for log in logs
            ],
            "total": total,
            "page": page,
            "limit": limit,
        }
