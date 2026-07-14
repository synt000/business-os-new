from sqlalchemy.orm import Session

from src.domains.permissions.models import (
    RolePermission,
    Permission,
    Role
)


def assign_permission(
    db: Session,
    role_name: str,
    permission_id: int
):

    role = (
        db.query(Role)
        .filter(
            Role.name == role_name
        )
        .first()
    )

    if not role:
        return None


    permission = (
        db.query(Permission)
        .filter(
            Permission.id == permission_id
        )
        .first()
    )

    if not permission:
        return None


    exists = (
        db.query(RolePermission)
        .filter(
            RolePermission.role_id == role.id,
            RolePermission.permission_id == permission.id
        )
        .first()
    )


    if exists:
        return exists


    mapping = RolePermission(
        role_id=role.id,
        permission_id=permission.id
    )

    db.add(mapping)
    db.commit()
    db.refresh(mapping)

    return mapping
