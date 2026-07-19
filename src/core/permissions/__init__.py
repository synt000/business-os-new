from fastapi import HTTPException, status, Depends

from src.models.saas_core import User
from src.core.security import get_current_user


async def require_owner_role(
    user: User = Depends(get_current_user)
):

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
