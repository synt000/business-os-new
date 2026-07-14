from src.core.database import SessionLocal
from src.domains.permissions.models import (
    Role,
    Permission,
    RolePermission
)


ROLE_MAP = {

    "OWNER": [
        "*"
    ],

    "ADMIN": [
        "users.view",
        "users.manage",
        "products.view",
        "products.manage",
        "orders.view",
        "orders.manage",
        "reports.view",
    ],

    "MANAGER": [
        "products.view",
        "products.manage",
        "orders.view",
        "orders.manage",
        "reports.view",
    ],

    "STAFF": [
        "products.view",
        "orders.view",
        "orders.create",
    ],

    "CASHIER": [
        "orders.view",
        "orders.create",
    ],

}


def seed_role_permissions():

    db = SessionLocal()

    try:

        for role_name, permissions in ROLE_MAP.items():

            role = (
                db.query(Role)
                .filter(Role.name == role_name)
                .first()
            )

            if not role:
                continue


            for perm_code in permissions:

                if perm_code == "*":

                    all_permissions = db.query(Permission).all()

                    for permission in all_permissions:

                        exists = (
                            db.query(RolePermission)
                            .filter(
                                RolePermission.role_id == role.id,
                                RolePermission.permission_id == permission.id
                            )
                            .first()
                        )

                        if not exists:

                            db.add(
                                RolePermission(
                                    role_id=role.id,
                                    permission_id=permission.id
                                )
                            )

                    continue


                permission = (
                    db.query(Permission)
                    .filter(Permission.code == perm_code)
                    .first()
                )


                if permission:

                    exists = (
                        db.query(RolePermission)
                        .filter(
                            RolePermission.role_id == role.id,
                            RolePermission.permission_id == permission.id
                        )
                        .first()
                    )

                    if not exists:

                        db.add(
                            RolePermission(
                                role_id=role.id,
                                permission_id=permission.id
                            )
                        )


        db.commit()

        print("✅ Role Permission Mapping Completed")


    finally:
        db.close()


if __name__ == "__main__":
    seed_role_permissions()
