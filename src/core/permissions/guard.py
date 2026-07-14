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

        # OWNER FULL ACCESS
        if current_user.role == "OWNER":
            return current_user


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


        # USER PERSONAL OVERRIDE CHECK
        user_permission = (
            db.query(UserPermission)
            .filter(
                UserPermission.user_id == current_user.id,
                UserPermission.permission_id == permission.id
            )
            .first()
        )


        if user_permission:
            return current_user



        # ROLE PERMISSION CHECK

        role = (
            db.query(Role)
            .filter(
                Role.name == current_user.role
            )
            .first()
        )


        if not role:
            raise HTTPException(
                status_code=403,
                detail="Role not found"
            )


        access = (
            db.query(RolePermission)
            .filter(
                RolePermission.role_id == role.id,
                RolePermission.permission_id == permission.id
            )
            .first()
        )


        if not access:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied"
            )


        return current_user


    return checker
