import os
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

# Authoritative Connection Layer Mappings
from ..database import get_db
from ..models.saas_core import User, Tenant, SubscriptionTier, BillingReceipt
from ..config.security import get_password_hash, verify_password, create_access_token, create_refresh_token, verify_access_token, get_current_user

router = APIRouter(tags=["Authentication Gateway Matrix"])

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

class TenantRegisterInboundSchema(BaseModel):
    company_name: str
    email: EmailStr
    password: str

class UserLoginInboundSchema(BaseModel):
    email: EmailStr
    password: str

class TokenRefreshInboundSchema(BaseModel):
    refresh_token: str

class BillingSlipSubmitInboundSchema(BaseModel):
    slip_base64_data: str

# 1. CORE HTML VIEW INTERFACES (ACCESSIBLE VIA /auth PATHWAYS)
@router.get("/auth/register", response_class=HTMLResponse)
async def render_register_page(request: Request):
    """Render Register Page UI Node"""
    return templates.TemplateResponse(request=request, name="register.html")

@router.get("/auth/login", response_class=HTMLResponse)
async def render_login_page(request: Request):
    """Render Login Page UI Node"""
    return templates.TemplateResponse(request=request, name="login.html")

# ==========================================================================
# 2. STANDARDIZED API PIPELINES BOUND TO SYSTEM PREFIXES (/api/v4/auth)
# ==========================================================================
@router.post("/api/v4/auth/tenant/onboard", status_code=status.HTTP_201_CREATED)
async def onboard_enterprise_workspace(payload: TenantRegisterInboundSchema, db: Session = Depends(get_db)):
    """Onboard Enterprise Workspace Engine"""
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
    """Authenticate User Session & Issue Dual JWT Claims Layer"""
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
    refresh_token = create_refresh_token(data=token_claims)
    
    return {
        "token_type": "bearer",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "tenant_id": target_user.tenant_id,
        "role": target_user.role
    }

@router.post("/api/v4/auth/refresh")
async def rotate_expired_access_token(payload: TokenRefreshInboundSchema, db: Session = Depends(get_db)):
    """Validates 7-Days Refresh Token claims and issues a brand-new short-lived Access Token"""
    token_claims = verify_access_token(payload.refresh_token)
    
    if token_claims is None or token_claims.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="INVALID_OR_EXPIRED_REFRESH_TOKEN")
        
    user_id = token_claims.get("user_id")
    tenant_id = token_claims.get("tenant_id")
    
    active_user = db.query(User).filter(User.id == user_id, User.tenant_id == tenant_id).first()
    if not active_user or not active_user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="ACCOUNT_SUSPENDED_OR_WORKSPACE_LOCKED")
        
    new_claims = {
        "sub": active_user.email,
        "user_id": active_user.id,
        "tenant_id": active_user.tenant_id,
        "role": active_user.role
    }
    
    new_access_token = create_access_token(data=new_claims)
    return {
        "token_type": "bearer",
        "access_token": new_access_token
    }

@router.post("/api/v4/auth/billing/submit", status_code=status.HTTP_201_CREATED)
async def submit_manual_billing_slip(payload: BillingSlipSubmitInboundSchema, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Receives and stores cross-platform payment receipt base64 logs bound safely to the tenant space."""
    if not payload.slip_base64_data.strip():
        raise HTTPException(status_code=422, detail="VALIDATION_ERROR: SLIP_DATA_CANNOT_BE_EMPTY")
        
    receipt_id = f"rcpt_{int(datetime.utcnow().timestamp())}"
    new_receipt = BillingReceipt(
        id=receipt_id, slip_base64_data=payload.slip_base64_data,
        verification_status="PENDING", tenant_id=current_user.tenant_id
    )
    db.add(new_receipt)
    
    try:
        db.commit()
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"TRANSACTION_FAILED: {str(exc)}")
        
    return {"status": "BILLING_RECEIPT_SUBMITTED_SUCCESSFULLY", "receipt_id": receipt_id, "verification_state": "PENDING"}

# ==========================================================================
# PRODUCTION NEW SUITE: HARDENED SYSTEM SUPERADMIN CONTROL PANELS APIs
# ==========================================================================
@router.get("/api/v4/superadmin/receipts")
async def superadmin_fetch_all_pending_receipts(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Allows only authenticated SUPERADMIN roles to fetch all inbound tenant billing screenshots."""
    if current_user.role != "SUPERADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="ACCESS_DENIED: SUPERADMIN_AUTHORITY_REQUIRED")
        
    pending_slips = db.query(BillingReceipt).filter(BillingReceipt.verification_status == "PENDING").all()
    return {
        "scope": "SUPERADMIN_PENDING_AUDIT_STREAM",
        "total_pending": len(pending_slips),
        "receipts": [{"id": r.id, "tenant_id": r.tenant_id, "submitted_at": r.submitted_at, "base64_blob": r.slip_base64_data} for r in pending_slips]
    }

@router.post("/api/v4/superadmin/tenants/{tenant_id}/approve")
async def superadmin_approve_and_unlock_tenant_workspace(tenant_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Approves a tenant billing receipt, resets the trial clock ceiling, and unlocks their business workspace."""
    if current_user.role != "SUPERADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="ACCESS_DENIED: SUPERADMIN_AUTHORITY_REQUIRED")
        
    target_tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not target_tenant:
        raise HTTPException(status_code=404, detail="TARGET_TENANT_NOT_FOUND")
        
    # PRODUCTION MATRIX: Reset trial clocks and elevate to paid tier natively
    target_tenant.trial_expired = False
    target_tenant.subscription_tier = SubscriptionTier.STARTUP  # Elevate from Free Trial to Startup Plan
    target_tenant.created_at = datetime.utcnow()                # Refresh baseline timestamps clock for subscription periods
    
    # Mark corresponding receipts as APPROVED cleanly
    db.query(BillingReceipt).filter(BillingReceipt.tenant_id == tenant_id, BillingReceipt.verification_status == "PENDING").update({"verification_status": "APPROVED"})
    
    try:
        db.commit()
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"SUPERADMIN_TRANSACTION_FAILED: {str(exc)}")
        
    return {"status": "TENANT_WORKSPACE_SUCCESSFULLY_APPROVED_AND_UNLOCKED", "tenant_id": tenant_id, "active_tier": "STARTUP"}
