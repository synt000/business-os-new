import os
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

# Authoritative Imports Context Mappings
from ..database import get_db
from ..models.saas_core import User, Tenant, SubscriptionTier
from ..config.security import get_password_hash, verify_password, create_access_token

router = APIRouter(tags=["Authentication Gateway Matrix"])

# Resolve dynamic configuration paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

class TenantRegisterInboundSchema(BaseModel):
    company_name: str
    email: EmailStr
    password: str

class UserLoginInboundSchema(BaseModel):
    email: EmailStr
    password: str

# 1. INDEPENDENT VIEW INTERFACES: FULLY ACCESSIBLE BY CONSUMERS WITHOUT PREFIX LEAKS
@router.get("/auth/register", response_class=HTMLResponse)
async def render_register_page(request: Request):
    return templates.TemplateResponse(request=request, name="register.html")

@router.get("/auth/login", response_class=HTMLResponse)
async def render_login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

# ==========================================================================
# PHASE 1 & 2 SECURE ENDPOINTS LAYER BOUND TO AUTHORITATIVE PREFIX PATHS
# ==========================================================================
@router.post("/api/v4/auth/tenant/onboard", status_code=status.HTTP_201_CREATED)
async def onboard_enterprise_workspace(payload: TenantRegisterInboundSchema, db: Session = Depends(get_db)):
    if not payload.company_name.strip() or not payload.password.strip():
        raise HTTPException(status_code=422, detail="CRITICAL_FAULT: PARAMETERS_CANNOT_BE_EMPTY")

    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="IDENTITY_CLASH: WORK_EMAIL_ALREADY_REGISTERED")

    tenant_id = f"tnt_{int(datetime.utcnow().timestamp())}"
    new_tenant = Tenant(
        id=tenant_id, company_name=payload.company_name, owner_email=payload.email,
        subscription_tier=SubscriptionTier.FREE_TRIAL, is_billing_active=True, trial_expired=False
    )
    db.add(new_tenant)

    user_id = f"usr_{int(datetime.utcnow().timestamp())}"
    encrypted_secure_hash = get_password_hash(payload.password)
    
    new_master_user = User(
        id=user_id, email=payload.email, hashed_password=encrypted_secure_hash,
        full_name=payload.company_name + " Admin", role="ADMIN", is_active=True, tenant_id=tenant_id
    )
    db.add(new_master_user)

    try:
        db.commit()
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"DATABASE_TRANSACTION_FAILED: {str(exc)}")

    return {"status": "TENANT_SUCCESSFULLY_INITIALIZED", "tenant_id": tenant_id, "admin_user_id": user_id, "trial_tier_active": True}

@router.post("/api/v4/auth/login")
async def authenticate_user_session(payload: UserLoginInboundSchema, db: Session = Depends(get_db)):
    target_user = db.query(User).filter(User.email == payload.email).first()
    if not target_user or not target_user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="AUTHENTICATION_FAILED: INVALID_CREDENTIALS")

    if not verify_password(payload.password, target_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="AUTHENTICATION_FAILED: INVALID_CREDENTIALS")

    token_claims = {
        "sub": target_user.email,
        "user_id": target_user.id,
        "tenant_id": target_user.tenant_id,
        "role": target_user.role
    }

    access_token = create_access_token(data=token_claims)
    return {
        "token_type": "bearer",
        "access_token": access_token,
        "tenant_id": target_user.tenant_id,
        "role": target_user.role
    }
