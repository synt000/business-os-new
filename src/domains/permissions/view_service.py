from sqlalchemy.orm import Session

from src.domains.permissions.models import (
    Role,
    RolePermission,
    Permission
)


def get_role_permissions(
    db: Session,
    role_name: str
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


    permissions = (
        db.query(Permission)
        .join(
            RolePermission,
            RolePermission.permission_id == Permission.id
        )
        .filter(
            RolePermission.role_id == role.id
        )
        .all()
    )


    return {
        "role": role.name,
        "permissions": [
            {
                "id": p.id,
                "code": p.code,
                "module": p.module
            }
            for p in permissions
        ]
    }
