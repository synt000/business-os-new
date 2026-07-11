from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from src.core.database import get_db
from src.core.security import (
    verify_refresh_token,
    create_access_token,
    create_refresh_token,
)
from src.models.saas_core import User
from src.security.refresh_manager import (
    verify_refresh_session,
    revoke_refresh_session,
    create_refresh_session,
)

router = APIRouter(
    prefix="/api/v4/auth",
    tags=["Refresh Token"],
)


class RefreshRequest(BaseModel):
    refresh_token: str


@router.post("/refresh")
def refresh_access_token(
    payload: RefreshRequest,
    db: Session = Depends(get_db),
):
    claims = verify_refresh_token(payload.refresh_token)

    if not claims:
        raise HTTPException(
            status_code=401,
            detail="INVALID_REFRESH_TOKEN"
        )

    user = db.query(User).filter(
        User.id == claims["user_id"]
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="USER_NOT_FOUND"
        )

    session = verify_refresh_session(
        db,
        payload.refresh_token
    )

    if not session:
        raise HTTPException(
            status_code=401,
            detail="REFRESH_TOKEN_REVOKED"
        )

    revoke_refresh_session(
        db,
        payload.refresh_token
    )

    token_claims = {
        "user_id": user.id,
        "tenant_id": user.tenant_id,
        "role": user.role,
    }

    access_token = create_access_token(token_claims)
    refresh_token = create_refresh_token(token_claims)

    create_refresh_session(
        db=db,
        user=user,
        refresh_token=refresh_token,
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
