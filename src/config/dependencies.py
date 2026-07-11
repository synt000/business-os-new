from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from ..database import get_db
from ..models.saas_core import User
from .security import SECRET_KEY, ALGORITHM


# Standard OAuth2 Ingress Extraction Token Matrix
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v4/auth/token",
    auto_error=False
)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="COULD_NOT_VALIDATE_CREDENTIALS",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not token:
        raise credentials_exception

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        tenant_id: str = payload.get("tenant_id")
        user_id: str = payload.get("user_id")

        if tenant_id is None or user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception


    active_user = db.query(User).filter(
        User.id == user_id,
        User.tenant_id == tenant_id
    ).first()


    if not active_user or not active_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ACCOUNT_SUSPENDED_OR_INACTIVE"
        )


    return active_user
