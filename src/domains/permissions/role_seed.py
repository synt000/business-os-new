from src.core.database import SessionLocal
from src.domains.permissions.models import Role


ROLES = [
    ("OWNER", "Full platform access"),
    ("ADMIN", "Administrator access"),
    ("MANAGER", "Business manager access"),
    ("STAFF", "Limited staff access"),
    ("CASHIER", "Cashier access"),
]


def seed_roles():

    db = SessionLocal()

    try:

        for name, desc in ROLES:

            exists = (
                db.query(Role)
                .filter(Role.name == name)
                .first()
            )

            if not exists:

                db.add(
                    Role(
                        name=name,
                        description=desc
                    )
                )

        db.commit()

        print("✅ Role Seed Completed")

    finally:
        db.close()


if __name__ == "__main__":
    seed_roles()
