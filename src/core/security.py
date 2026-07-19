import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.core.config import settings
from src.core.database import get_db
from src.models.saas_core import User, Tenant
from src.domains.subscription.models import Subscription

# 1. 5-STAR UPGRADE: ENFORCE SECURE ARGON2 PASSWORD CRYPTOGRAPHY Context
PWD_CONTEXT = CryptContext(schemes=["argon2"], deprecated="auto")

# ALIGN OAUTH2 GATEWAY CONFIG EXPLICITLY TO DUAL FORM/JSON SYSTEM PATHWAY
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_VERSION_PREFIX}/auth/token", auto_error=False)

def get_password_hash(password: str) -> str:
    return PWD_CONTEXT.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return PWD_CONTEXT.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # 2. OWASP ENTERPRISE STANDARD CLAIMS INGESTION MATRIX
    to_encode.update({
        "exp": expire,
        "type": "access",
        "iss": settings.TOKEN_ISSUER,
        "aud": settings.TOKEN_AUDIENCE,
        "iat": now,
        "nbf": now,
        "jti": f"jti_{secrets.token_hex(16)}"
    })
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    expire = now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({
        "exp": expire,
        "type": "refresh",
        "iss": settings.TOKEN_ISSUER,
        "aud": settings.TOKEN_AUDIENCE,
        "iat": now,
        "nbf": now,
        "jti": f"jti_{secrets.token_hex(16)}"
    })
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verify_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM], audience=settings.TOKEN_AUDIENCE)
        return payload if payload.get("type") == "access" else None
    except JWTError:
        return None

def verify_refresh_token(token: str) -> Optional[dict]:
    """Decodes and validates long-lived cryptographic refresh token chains."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM], audience=settings.TOKEN_AUDIENCE)
        return payload if payload.get("type") == "refresh" else None
    except JWTError:
        return None

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="COULD_NOT_VALIDATE_SECURE_JWT_CREDENTIALS",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise credentials_exception
    payload = verify_access_token(token)
    if payload is None:
        raise credentials_exception
        
    user_id: str = payload.get("user_id")
    tenant_id: str = payload.get("tenant_id")
    if not user_id or not tenant_id:
        raise credentials_exception
        
    active_user = db.query(User).filter(User.id == user_id, User.tenant_id == tenant_id).first()
    if not active_user or not active_user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="ACCOUNT_SUSPENDED_OR_INACTIVE")
        
    subscription = (
        db.query(Subscription)
        .filter(
            Subscription.tenant_id == active_user.tenant_id,
            Subscription.status == "ACTIVE"
        )
        .first()
    )

    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="WORKSPACE_LOCKED: SUBSCRIPTION_EXPIRED"
        )

    if subscription.end_date:
        if subscription.end_date < datetime.utcnow():

            subscription.status = "EXPIRED"
            db.commit()

            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail="WORKSPACE_LOCKED: TRIAL_EXPIRED"
            )
    return active_user

# ==========================================================
# JWT DECODE HELPER
# ==========================================================

def decode_token(token: str):
    """
    Decode JWT access/refresh token
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            audience=settings.TOKEN_AUDIENCE
        )
        return payload

    except Exception as e:
        print("JWT DECODE ERROR:", e)
        return None



def decode_token(token: str):
    """
    Decode JWT token and validate audience.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            audience=settings.TOKEN_AUDIENCE
        )
        return payload

    except Exception:
        return None
