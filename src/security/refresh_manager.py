from datetime import datetime
from jose import jwt

from sqlalchemy.orm import Session

from src.core.config import settings
from src.models.refresh_token import RefreshToken


def create_refresh_session(
    db: Session,
    user,
    refresh_token: str,
):
    payload = jwt.decode(
        refresh_token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
        audience=settings.TOKEN_AUDIENCE,
    )

    token = RefreshToken(
        user_id=user.id,
        tenant_id=user.tenant_id,
        jti=payload["jti"],
        expires_at=datetime.fromtimestamp(payload["exp"]),
        revoked=False,
    )

    db.add(token)
    db.commit()
    db.refresh(token)

    return token


def verify_refresh_session(
    db: Session,
    refresh_token: str,
):
    payload = jwt.decode(
        refresh_token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
        audience=settings.TOKEN_AUDIENCE,
    )

    return (
        db.query(RefreshToken)
        .filter(
            RefreshToken.jti == payload["jti"],
            RefreshToken.revoked == False,
        )
        .first()
    )


def revoke_refresh_session(
    db: Session,
    refresh_token: str,
):
    payload = jwt.decode(
        refresh_token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
        audience=settings.TOKEN_AUDIENCE,
    )

    token = (
        db.query(RefreshToken)
        .filter(RefreshToken.jti == payload["jti"])
        .first()
    )

    if token:
        token.revoked = True
        token.revoked_at = datetime.utcnow()
        db.commit()
