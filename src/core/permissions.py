from fastapi import HTTPException, status

from src.models.saas_core import User


def require_owner_role(user: User):

    allowed_roles = [
        "OWNER",
        "SUPER_ADMIN",
        "ADMIN"
    ]

    if user.role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Owner access required"
        )

    return user
