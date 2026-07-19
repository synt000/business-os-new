from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user
from src.models.saas_core import User

from src.domains.permissions.models import (
    Role,
    Permission,
    RolePermission,
    UserPermission
)


def require_permission(permission_code: str):

    def checker(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):

        permission = (
            db.query(Permission)
            .filter(
                Permission.code == permission_code
            )
            .first()
        )

        if not permission:
            raise HTTPException(
                status_code=404,
                detail="Permission not found"
            )


        # =========================
        # USER PERSONAL OVERRIDE
        # =========================

        user_permission = (
            db.query(UserPermission)
            .filter(
                UserPermission.user_id == current_user.id,
                UserPermission.permission_id == permission.id
            )
            .first()
        )

        if user_permission:

            if user_permission.is_allowed == 1:
                return current_user

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission explicitly denied"
            )



        # =========================
        # ROLE PERMISSION
        # =========================

        role = (
            db.query(Role)
            .filter(
                Role.name == current_user.role
            )
            .first()
        )


        if role:

            access = (
                db.query(RolePermission)
                .filter(
                    RolePermission.role_id == role.id,
                    RolePermission.permission_id == permission.id
                )
                .first()
            )

            if access:
                return current_user



        # =========================
        # OWNER FALLBACK
        # =========================

        if current_user.role == "OWNER":
            return current_user



        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )


    return checker
