from datetime import datetime, timezone

from sqlalchemy.orm import Session

from src.domains.audit.models import AuditLog


class AuditService:

    @staticmethod
    def create_audit_log(
        db: Session,
        tenant_id: str,
        action: str,
        table_name: str,
        record_id: str,
        changes: str | None = None,
        user_id: str | None = None,
    ):
        audit = AuditLog(
            tenant_id=tenant_id,
            action=action,
            table_name=table_name,
            record_id=record_id,
            changes=changes,
            user_id=user_id,
        )

        db.add(audit)

        return audit

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


    @staticmethod
    def get_audit_summary(
        db: Session,
        tenant_id: str,
    ):

        now = datetime.now(timezone.utc)

        today_start = now.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

        base = (
            db.query(AuditLog)
            .filter(
                AuditLog.tenant_id == tenant_id
            )
        )

        return {
            "total_events": base.count(),

            "today_events": (
                base.filter(
                    AuditLog.created_at >= today_start
                )
                .count()
            ),

            "admin_actions": (
                base.filter(
                    AuditLog.action.ilike("%admin%")
                )
                .count()
            ),

            "business_changes": (
                base.filter(
                    AuditLog.table_name.isnot(None)
                )
                .count()
            ),
        }


    @staticmethod
    def get_activity_metrics(
        db: Session,
        tenant_id: str,
    ):

        base = (
            db.query(AuditLog)
            .filter(
                AuditLog.tenant_id == tenant_id
            )
        )

        return {
            "product_activity": (
                base.filter(
                    AuditLog.table_name.ilike("%product%")
                )
                .count()
            ),

            "order_activity": (
                base.filter(
                    AuditLog.table_name.ilike("%order%")
                )
                .count()
            ),

            "invoice_activity": (
                base.filter(
                    AuditLog.table_name.ilike("%invoice%")
                )
                .count()
            ),

            "payment_activity": (
                base.filter(
                    AuditLog.table_name.ilike("%payment%")
                )
                .count()
            ),

            "admin_activity": (
                base.filter(
                    AuditLog.action.ilike("%admin%")
                )
                .count()
            ),
        }
