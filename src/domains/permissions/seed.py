from src.core.database import SessionLocal
from src.domains.permissions.models import (
    Role,
    Permission,
    RolePermission
)


PERMISSIONS = [
    "dashboard.view",
    "users.manage",
    "billing.manage",
    "tenant.delete",

    "inventory.manage",
    "inventory.view",

    "orders.manage",
    "orders.create",

    "customers.view",

    "reports.view",
]


ROLES = {
    "OWNER": [
        "dashboard.view",
        "users.manage",
        "billing.manage",
        "tenant.delete",
        "inventory.manage",
        "orders.manage",
        "reports.view",
    ],

    "ADMIN": [
        "dashboard.view",
        "users.manage",
        "inventory.manage",
        "orders.manage",
        "reports.view",
    ],

    "MANAGER": [
        "dashboard.view",
        "inventory.view",
        "orders.manage",
        "reports.view",
    ],

    "STAFF": [
        "orders.create",
        "customers.view",
        "inventory.view",
    ],
}


def seed_permissions():

    db = SessionLocal()

    try:

        permission_map = {}

        for name in PERMISSIONS:

            permission = (
                db.query(Permission)
                .filter(
                    Permission.code == name
                )
                .first()
            )

            if not permission:
                permission = Permission(
                    code=name
                )
                db.add(permission)
                db.commit()
                db.refresh(permission)

            permission_map[name] = permission


        for role_name, perms in ROLES.items():

            role = (
                db.query(Role)
                .filter(
                    Role.name == role_name
                )
                .first()
            )

            if not role:
                role = Role(
                    name=role_name
                )
                db.add(role)
                db.commit()
                db.refresh(role)


            for perm_name in perms:

                exists = (
                    db.query(RolePermission)
                    .filter(
                        RolePermission.role_id == role.id,
                        RolePermission.permission_id == permission_map[perm_name].id
                    )
                    .first()
                )

                if not exists:

                    db.add(
                        RolePermission(
                            role_id=role.id,
                            permission_id=permission_map[perm_name].id
                        )
                    )

            db.commit()


        print("✅ Permission Seed Completed")


    finally:
        db.close()


if __name__ == "__main__":
    seed_permissions()
