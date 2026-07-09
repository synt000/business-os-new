import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

PWD_CONTEXT = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY", "prod-business-os-enterprise-9.9-jwt-key-2026")
ALGORITHM = "HS256"

# CORE TOKENS LIFECYCLE SPECS MATRIX
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7
TRIAL_DURATION_DAYS = 3

# ==========================================================================
# PRODUCTION FIXED: AUTHORITATIVE OWNER DIRECT CONTACT MATRIX METRICS
# ==========================================================================
OWNER_TELEGRAM_LINK = os.getenv("OWNER_TELEGRAM_LINK", "https://t.me")
OWNER_SUPPORT_PHONE = os.getenv("OWNER_SUPPORT_PHONE", "+959450000000") # Protocol: tel:+95945...

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v4/auth/login", 
    auto_error=False
)

def get_password_hash(password: str) -> str:
    """Transforms raw text password into safe pbkdf2_sha256 database hashes."""
    return PWD_CONTEXT.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies plain password inputs against structural pbkdf2_sha256 database hashes."""
    return PWD_CONTEXT.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    """Generates standard secure short-lived multi-tenant access tokens."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict) -> str:
    """Generates hardened long-lived multi-tenant token rotation elements."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str) -> Optional[dict]:
    """Validates structural JWT claims and parses tenant contextual properties."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# PURE FASTAPI DEPENDENCY INJECTION BOUND TO GENUINE DATABASE ORM USER OBJECTS
async def get_current_user(token: str = Depends(oauth2_scheme)) -> object:
    from ..database import get_db
    from ..models.saas_core import User, Tenant, SubscriptionTier
    
    db = next(get_db())
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="COULD_NOT_VALIDATE_SECURE_JWT_CREDENTIALS",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if not token:
        raise credentials_exception
        
    payload = verify_access_token(token)
    if payload is None or payload.get("type") != "access":
        raise credentials_exception
        
    user_id: str = payload.get("user_id")
    tenant_id: str = payload.get("tenant_id")
    if user_id is None or tenant_id is None:
        raise credentials_exception
        
    active_user = db.query(User).filter(User.id == user_id, User.tenant_id == tenant_id).first()
    if not active_user or not active_user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="ACCOUNT_SUSPENDED_OR_INACTIVE")
        
    tenant_profile = db.query(Tenant).filter(Tenant.id == active_user.tenant_id).first()
    if tenant_profile:
        if tenant_profile.subscription_tier == SubscriptionTier.FREE_TRIAL:
            elapsed_timeline = datetime.utcnow() - tenant_profile.created_at
            if elapsed_timeline.days >= TRIAL_DURATION_DAYS or tenant_profile.trial_expired:
                if not tenant_profile.trial_expired:
                    tenant_profile.trial_expired = True
                    db.commit()
                raise HTTPException(
                    status_code=status.HTTP_402_PAYMENT_REQUIRED,
                    detail="WORKSPACE_LOCKED: FREE_TRIAL_EXPIRED_RENEWAL_REQUIRED"
                )
                
    return active_user
