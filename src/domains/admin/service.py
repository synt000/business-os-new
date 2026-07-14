from sqlalchemy.orm import Session

from src.models.saas_core import User
from src.core.security import get_password_hash


def list_admins(db: Session):
    return (
        db.query(User)
        .filter(
            User.role.in_([
                "OWNER",
                "ADMIN",
                "MANAGER",
                "STAFF"
            ])
        )
        .order_by(User.created_at.desc())
        .all()
    )


def create_admin(
    db: Session,
    payload
):
    user = User(
        email=payload.email,
        hashed_password=get_password_hash(payload.password),
        full_name=payload.full_name,
        role=payload.role,
        is_active=True,

        # ယာယီအတွက် OWNER နဲ့ tenant တူတူသုံးမယ်
        tenant_id="e4ca6dc4-9543-4c4f-ab8c-a39777f27b45"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
