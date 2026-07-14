from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.permissions.guard import require_permission

from src.domains.permissions.assign import PermissionAssign
from src.domains.permissions.remove import PermissionRemove
from src.domains.permissions.service import assign_permission


router = APIRouter(
    prefix="/permissions",
    tags=["Permissions"]
)


@router.post(
    "/assign",
    dependencies=[
        Depends(require_permission("users.manage"))
    ]
)
def assign_role_permission(
    data: PermissionAssign,
    db: Session = Depends(get_db)
):

    result = assign_permission(
        db,
        data.role_name,
        data.permission_id
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Role or Permission not found"
        )

    return {
        "status":"SUCCESS",
        "role_id": result.role_id,
        "permission_id": result.permission_id
    }


@router.get(
    "/role/{role_name}"
)
def view_role_permissions(
    role_name: str,
    current_user = Depends(
        require_permission("users.manage")
    ),
    db: Session = Depends(get_db),
):

    from src.domains.permissions.view_service import (
        get_role_permissions
    )

    result = get_role_permissions(
        db,
        role_name
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )

    return result


@router.delete(
    "/remove"
)
def remove_role_permission(
    data: PermissionRemove,
    current_user = Depends(
        require_permission("users.manage")
    ),
    db: Session = Depends(get_db),
):

    from src.domains.permissions.remove_service import (
        remove_permission
    )

    result = remove_permission(
        db,
        data.role_name,
        data.permission_id
    )


    if not result:
        raise HTTPException(
            status_code=404,
            detail="Permission mapping not found"
        )


    return {
        "status":"SUCCESS",
        **result
    }


@router.delete(
    "/remove"
)
def remove_role_permission(
    data: PermissionRemove,
    current_user = Depends(
        require_permission("users.manage")
    ),
    db: Session = Depends(get_db),
):

    from src.domains.permissions.remove_service import (
        remove_permission
    )

    result = remove_permission(
        db,
        data.role_name,
        data.permission_id
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Permission mapping not found"
        )

    return {
        "status": "SUCCESS",
        **result
    }
