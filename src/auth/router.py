from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import verify_password, create_access_token, create_refresh_token
from src.models.saas_core import User, Tenant

router = APIRouter(prefix="/api/v4/auth", tags=["Identity & Access Management"])

# ==========================================================================
# PYDANTIC INBOUND SCHEMAS SPECIFICATION V5.5
# ==========================================================================
class JSONLoginInboundPayload(BaseModel):
    email: EmailStr
    password: str

class TokenResponseOutboundPayload(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    workspace_id: str
    role_profile: str

# ==========================================================================
# GATEWAY NODE 1: SWAGGER UI OAUTH2 COMPLIANT FORM-DATA TOKEN INGRESS
# ==========================================================================
@router.post("/token", response_model=TokenResponseOutboundPayload)
async def authenticate_via_oauth2_form_flow(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    """Handles core Form-Data specifications emitted by Swagger UI Authorize controllers natively."""
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="INVALID_WORKSPACE_CREDENTIALS_COMBINATION")
        
    tenant = db.query(Tenant).filter(Tenant.id == user.tenant_id).first()
    if tenant and tenant.trial_expired:
        raise HTTPException(status_code=402, detail="WORKSPACE_LOCKED: FREE_TRIAL_EXPIRED")
        
    token_claims = {"user_id": user.id, "tenant_id": user.tenant_id, "role": user.role}
    return {
        "access_token": create_access_token(token_claims),
        "refresh_token": create_refresh_token(token_claims),
        "workspace_id": user.tenant_id,
        "role_profile": user.role
    }

# ==========================================================================
# GATEWAY NODE 2: ENTERPRISE MOBILE/WEB APP CLIENTS PURE JSON INGRESS
# ==========================================================================
@router.post("/login", response_model=TokenResponseOutboundPayload)
async def authenticate_via_pure_json_payload(
    payload: JSONLoginInboundPayload, 
    db: Session = Depends(get_db)
):
    """Processes standardized raw application/json login vectors from upstream UI clients cleanly."""
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="INVALID_WORKSPACE_CREDENTIALS_COMBINATION")
        
    tenant = db.query(Tenant).filter(Tenant.id == user.tenant_id).first()
    if tenant and tenant.trial_expired:
        raise HTTPException(status_code=402, detail="WORKSPACE_LOCKED: FREE_TRIAL_EXPIRED")
        
    token_claims = {"user_id": user.id, "tenant_id": user.tenant_id, "role": user.role}
    return {
        "access_token": create_access_token(token_claims),
        "refresh_token": create_refresh_token(token_claims),
        "workspace_id": user.tenant_id,
        "role_profile": user.role
    }
