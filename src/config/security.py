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
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# FIXED: FULLY ALIGNED TO PRODUCTION APIRUTER PREFIX FOR SWAGGER INTERACTION SECURELY
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v4/auth/login", 
    auto_error=False
)

def get_password_hash(password: str) -> str:
    """Transforms raw text password into pbkdf2_sha256 hashes cleanly."""
    return PWD_CONTEXT.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies plain password inputs against structural pbkdf2_sha256 database hashes."""
    return PWD_CONTEXT.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    """Generates standard secure short-lived multi-tenant access tokens."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str) -> Optional[dict]:
    """Validates structural JWT claims and parses tenant contextual properties."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# PRODUCTION FIXED: COMPLETELY REMOVED THE DATABASE SESSION TYPE HINT FROM THE ARGUMENTS TO PREVENT OPENAPI INJECTION CRASHES
async def get_current_user(token: str = Depends(oauth2_scheme)) -> object:
    from ..database import get_db
    from ..models.saas_core import User
    
    # Force context runtime evaluation to completely isolate Pydantic schema generation
    db = next(get_db())
        
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
    if user_id is None or tenant_id is None:
        raise credentials_exception
        
    # Enforce rigid database isolation lookup parameters tightly
    active_user = db.query(User).filter(User.id == user_id, User.tenant_id == tenant_id).first()
    if not active_user or not active_user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="ACCOUNT_SUSPENDED_OR_INACTIVE")
        
    return active_user
