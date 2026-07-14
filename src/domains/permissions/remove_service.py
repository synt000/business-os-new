from sqlalchemy.orm import Session

from src.domains.permissions.models import (
    Role,
    Permission,
    RolePermission
)


def remove_permission(
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


    mapping = (
        db.query(RolePermission)
        .filter(
            RolePermission.role_id == role.id,
            RolePermission.permission_id == permission_id
        )
        .first()
    )

    if not mapping:
        return None


    db.delete(mapping)
    db.commit()


    return {
        "role": role.name,
        "removed_permission_id": permission_id
    }
