from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.database import get_db
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

from src.domains.permissions.models import (
    UserPermission,
    Permission
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



# ======================================
# USER PERSONAL PERMISSION OVERRIDE
# ======================================


@router.get(
    "/users/{user_id}/permissions"
)
def get_user_permissions(
    user_id: str,
    current_user: User = Depends(
        require_permission("users.manage")
    ),
    db: Session = Depends(get_db),
):

    rows = (
        db.query(Permission)
        .join(
            UserPermission,
            UserPermission.permission_id == Permission.id
        )
        .filter(
            UserPermission.user_id == user_id
        )
        .all()
    )


    return {
        "user_id": user_id,
        "permissions": [
            {
                "id": p.id,
                "code": p.code,
                "module": p.module,
                "description": p.description
            }
            for p in rows
        ]
    }



@router.post(
    "/users/{user_id}/permissions/{permission_id}"
)
def add_user_permission(
    user_id: str,
    permission_id: int,
    current_user: User = Depends(
        require_permission("users.manage")
    ),
    db: Session = Depends(get_db),
):

    exists = (
        db.query(UserPermission)
        .filter(
            UserPermission.user_id == user_id,
            UserPermission.permission_id == permission_id
        )
        .first()
    )


    if exists:
        return {
            "status": "EXISTS"
        }


    row = UserPermission(
        user_id=user_id,
        permission_id=permission_id
    )


    db.add(row)
    db.commit()


    return {
        "status": "SUCCESS"
    }



@router.delete(
    "/users/{user_id}/permissions/{permission_id}"
)
def remove_user_permission(
    user_id: str,
    permission_id: int,
    current_user: User = Depends(
        require_permission("users.manage")
    ),
    db: Session = Depends(get_db),
):

    row = (
        db.query(UserPermission)
        .filter(
            UserPermission.user_id == user_id,
            UserPermission.permission_id == permission_id
        )
        .first()
    )


    if row:
        db.delete(row)
        db.commit()


    return {
        "status": "SUCCESS"
    }
