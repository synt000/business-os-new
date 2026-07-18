import uuid
import uuid
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token
from src.models.saas_core import User, Tenant
from src.domains.subscription.models import Subscription, SubscriptionPlan

from src.security.login_guard import (
    check_account_locked,
    register_failed_login,
    register_success_login
)

from src.security.event_logger import log_security_event
from src.security.session_manager import create_login_session
from src.security.refresh_manager import create_refresh_session


router = APIRouter(prefix="/api/v4/auth", tags=["Identity & Access Management"])

# ==========================================================
# LOGIN SECURITY HARDENING LAYER
# ==========================================================







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

class RegisterInboundPayload(BaseModel):
    company_name: str
    email: EmailStr
    password: str
    full_name: str | None = None

# ==========================================================================
# GATEWAY NODE 1: SWAGGER UI OAUTH2 COMPLIANT FORM-DATA TOKEN INGRESS
# ==========================================================================
@router.post("/token", response_model=TokenResponseOutboundPayload)
async def authenticate_via_oauth2_form_flow(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Handles core Form-Data specifications emitted by Swagger UI Authorize controllers natively."""
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=401,
            detail="INVALID_WORKSPACE_CREDENTIALS_COMBINATION"
        )

    check_account_locked(user)

    if not verify_password(form_data.password, user.hashed_password):

        register_failed_login(db, user)

        raise HTTPException(
            status_code=401,
            detail="INVALID_WORKSPACE_CREDENTIALS_COMBINATION"
        )

    register_success_login(db, user)

    create_login_session(
        db=db,
        user=user,
        ip_address=request.client.host if request.client else "UNKNOWN",
        user_agent=request.headers.get("user-agent","UNKNOWN"),
        device_name=request.headers.get("user-agent","UNKNOWN"),
    )

            
    tenant = db.query(Tenant).filter(Tenant.id == user.tenant_id).first()
    if tenant and tenant.trial_expired:
        raise HTTPException(status_code=402, detail="WORKSPACE_LOCKED: FREE_TRIAL_EXPIRED")
        
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
    request: Request,
    payload: JSONLoginInboundPayload,
    db: Session = Depends(get_db)
):
    """Processes standardized raw application/json login vectors from upstream UI clients cleanly."""
    print("========== LOGIN DEBUG ==========", flush=True)
    print("EMAIL:", payload.email, flush=True)
    print("EMAIL REPR:", repr(payload.email), flush=True)
    print("EMAIL TYPE:", type(payload.email), flush=True)
    print("ENGINE =", db.get_bind(), flush=True)
    print("DB URL =", db.get_bind().engine.url, flush=True)
    print("USER COUNT =", db.query(User).count(), flush=True)

    user = db.query(User).filter(User.email == payload.email).first()

    print("QUERY EMAIL:", payload.email, flush=True)
    print("ALL EMAILS:", [u.email for u in db.query(User).all()], flush=True)
    print("USER FOUND:", user is not None, flush=True)

    if user:
        print("PASSWORD VERIFY:", verify_password(payload.password, user.hashed_password), flush=True)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="INVALID_WORKSPACE_CREDENTIALS_COMBINATION"
        )

    check_account_locked(user)

    if not verify_password(payload.password, user.hashed_password):

        register_failed_login(db, user)

        raise HTTPException(
            status_code=401,
            detail="INVALID_WORKSPACE_CREDENTIALS_COMBINATION"
        )

    register_success_login(db, user)
        
    tenant = db.query(Tenant).filter(Tenant.id == user.tenant_id).first()

    if tenant and tenant.trial_expired:
        raise HTTPException(
            status_code=402,
            detail="WORKSPACE_LOCKED: FREE_TRIAL_EXPIRED"
        )

    token_claims = {
        "user_id": user.id,
        "tenant_id": user.tenant_id,
        "role": user.role
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
        "access_token": create_access_token(token_claims),
        "refresh_token": create_refresh_token(token_claims),
        "workspace_id": user.tenant_id,
        "role_profile": user.role
    }


# ==========================================================================
# BUSINESS OWNER REGISTRATION + FREE TRIAL ACTIVATION
# ==========================================================================
# ==========================================================================
# BUSINESS OWNER REGISTRATION + FREE TRIAL ACTIVATION
# ==========================================================================
class RegisterInboundPayload(BaseModel):
    company_name: str
    email: EmailStr
    password: str
    full_name: str | None = None


@router.post("/register")
async def register_business_owner(
    payload: RegisterInboundPayload,
    db: Session = Depends(get_db)
):

    print("STEP 1", flush=True)

    existing = db.query(User).filter(
        User.email == payload.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="EMAIL_ALREADY_REGISTERED"
        )


    tenant = Tenant(
        company_name=payload.company_name,
        owner_email=payload.email,
        subscription_tier="FREE_TRIAL",
        is_billing_active=True
    )

    print("STEP 3", flush=True)

    db.add(tenant)
    db.commit()

    print("STEP 4", flush=True)
    db.refresh(tenant)

    print("STEP 5", flush=True)


    user = User(
        email=payload.email,
        hashed_password=get_password_hash(payload.password),
        full_name=payload.full_name,
        role="OWNER",
        tenant_id=tenant.id
    )

    print("STEP 6", flush=True)

    db.add(user)
    db.commit()

    print("STEP 7", flush=True)
    db.refresh(user)


    print("STEP 8", flush=True)

    trial_plan = db.query(SubscriptionPlan).filter(
        SubscriptionPlan.name == "FREE_TRIAL"
    ).first()


    if trial_plan:

        subscription = Subscription(
        id=str(uuid.uuid4()),
            tenant_id=tenant.id,
            plan_id=trial_plan.id,
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=3),
            status="ACTIVE",
            is_trial=True
        )

        db.add(subscription)
        db.commit()


    return {
        "message": "BUSINESS_WORKSPACE_CREATED",
        "tenant_id": tenant.id,
        "owner": user.email,
        "subscription": "FREE_TRIAL",
        "trial_days": 3
    }
