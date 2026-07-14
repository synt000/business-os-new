from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user
from src.core.permissions.guard import require_permission

from src.models.saas_core import User

from src.domains.admin.schemas import (
    AdminCreate,
    AdminResponse,
)

from src.domains.admin.service import (
    create_admin,
    list_admins as service_list_admins,
)

router = APIRouter(
    prefix="/admin",
    tags=["Admin Management"]
)


@router.get(
    "/users",
    response_model=list[AdminResponse]
)
def get_admin_users(
    current_user: User = Depends(
        require_permission("users.view")
    ),
    db: Session = Depends(get_db),
):
    return service_list_admins(db)


@router.post(
    "/users",
    response_model=AdminResponse
)
def create_admin_user(
    admin: AdminCreate,
    current_user: User = Depends(
        require_permission("users.manage")
    ),
    db: Session = Depends(get_db),
):
    return create_admin(
        db,
        admin
    )
