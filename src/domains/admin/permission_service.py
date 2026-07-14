from sqlalchemy.orm import Session

from src.models.saas_core import User
from src.domains.permissions.models import (
    Permission,
    UserPermission
)


def get_user_permissions(
    db: Session,
    user_id: str
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

    return rows



def assign_user_permission(
    db: Session,
    user_id: str,
    permission_id: int
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
        return exists


    row = UserPermission(
        user_id=user_id,
        permission_id=permission_id
    )

    db.add(row)
    db.commit()
    db.refresh(row)

    return row



def remove_user_permission(
    db: Session,
    user_id: str,
    permission_id: int
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

    return row
