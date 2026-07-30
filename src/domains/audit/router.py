from fastapi import (
    APIRouter,
    Depends,
    Query
)

from sqlalchemy.orm import Session

from src.database import get_db
from src.core.security import get_current_user

from src.domains.audit.service import AuditService


router = APIRouter(
    prefix="/api/v4/audit",
    tags=["Audit"]
)


@router.get("/logs")
def get_audit_logs(
    page: int = Query(
        1,
        ge=1
    ),
    limit: int = Query(
        20,
        ge=1,
        le=100
    ),
    action: str | None = None,
    table_name: str | None = None,
    user_id: str | None = None,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    return AuditService.get_audit_logs(
        db=db,
        tenant_id=current_user.tenant_id,
        page=page,
        limit=limit,
        action=action,
        table_name=table_name,
        user_id=user_id,
    )


from src.domains.audit.service import get_audit_summary


@router.get("/summary")
def audit_summary(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_audit_summary(
        db=db,
        tenant_id=current_user.tenant_id
    )
