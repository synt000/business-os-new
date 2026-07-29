import uuid
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token
from src.models.saas_core import User, Tenant, BusinessType
from src.models.business_profile import BusinessProfile
from src.domains.business_type.services.feature_assign_service import assign_features_to_tenant
from src.domains.business_type.services.slug_service import generate_business_slug
from src.domains.subscription.models import Subscription, SubscriptionPlan

from src.security.login_guard import (
    check_account_locked,
    register_failed_login,
    register_success_login
)

from src.security.event_logger import log_security_event
from src.auth.device_service import register_device
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

    # Identity Security v5.8 Device Fingerprint
    device_fingerprint: str | None = None
    device_name: str | None = None
    platform: str | None = None
    browser: str | None = None
    screen_width: str | None = None
    screen_height: str | None = None
    timezone_name: str | None = None
    language: str | None = None

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
    business_type_code: str


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

    device_session_id = None

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
        "business_type": tenant.business_type_id if tenant else None,
        "subscription": tenant.subscription_tier.value if tenant else None,
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

    user = db.query(User).filter(User.email == payload.email).first()


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
        

    # Identity Security v5.8 Device Registration
    if payload.device_fingerprint:

        device, is_new = register_device(
            db,
            workspace_id=user.tenant_id,
            device_fingerprint=payload.device_fingerprint,
            device_name=payload.device_name,
            platform=payload.platform,
            browser=payload.browser,
            screen_width=payload.screen_width,
            screen_height=payload.screen_height,
            timezone_name=payload.timezone_name,
            language=payload.language,
            ip_address=request.client.host if request.client else "UNKNOWN",
            user_agent=request.headers.get(
                "user-agent",
                "UNKNOWN"
            ),
        )

        device_session_id = device.id

        log_security_event(
            db,
            event_type=(
                "DEVICE_REGISTERED"
                if is_new
                else "DEVICE_UPDATED"
            ),
            user_id=user.id,
            tenant_id=user.tenant_id,
            request=request,
            device_info={
                "fingerprint": payload.device_fingerprint,
                "platform": payload.platform,
                "browser": payload.browser,
                "screen": (
                    f"{payload.screen_width}x{payload.screen_height}"
                ),
                "timezone": payload.timezone_name,
            },
            description="Identity device registration flow",
        )


        device_info = {
            "fingerprint": payload.device_fingerprint,
            "platform": payload.platform,
            "browser": payload.browser,
            "screen": (
                f"{payload.screen_width}x{payload.screen_height}"
            ),
            "timezone": payload.timezone_name,
        }


        if device.is_blocked:

            log_security_event(
                db,
                event_type="DEVICE_BLOCKED",
                user_id=user.id,
                tenant_id=user.tenant_id,
                request=request,
                device_info=device_info,
                description="Blocked device login rejected",
            )

            raise HTTPException(
                status_code=403,
                detail="DEVICE_BLOCKED"
            )


        if is_new:

            log_security_event(
                db,
                event_type="NEW_DEVICE_LOGIN",
                user_id=user.id,
                tenant_id=user.tenant_id,
                request=request,
                device_info={
                    "fingerprint": payload.device_fingerprint,
                    "platform": payload.platform,
                    "browser": payload.browser,
                    "screen": (
                        f"{payload.screen_width}x{payload.screen_height}"
                    ),
                    "timezone": payload.timezone_name,
                },
                description="New device successful login detected",
            )


    tenant = db.query(Tenant).filter(Tenant.id == user.tenant_id).first()

    if tenant and tenant.trial_expired:
        raise HTTPException(
            status_code=402,
            detail="WORKSPACE_LOCKED: FREE_TRIAL_EXPIRED"
        )

    create_login_session(
        db=db,
        user=user,
        ip_address=request.client.host if request.client else "UNKNOWN",
        user_agent=request.headers.get(
            "user-agent",
            "UNKNOWN"
        ),
        device_name=payload.device_name or "UNKNOWN",
        device_session_id=device_session_id,
    )

    token_claims = {
        "user_id": user.id,
        "tenant_id": user.tenant_id,
        "role": user.role,
        "business_type": tenant.business_type_id if tenant else None,
        "subscription": tenant.subscription_tier.value if tenant else None,
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
        "workspace_id": user.tenant_id,
        "role_profile": user.role
    }


# ==========================================================================
# BUSINESS OWNER REGISTRATION + FREE TRIAL ACTIVATION
# ==========================================================================
# ==========================================================================
# BUSINESS OWNER REGISTRATION + FREE TRIAL ACTIVATION
# ==========================================================================


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


    business_type = (
        db.query(BusinessType)
        .filter(
            BusinessType.code == payload.business_type_code
        )
        .first()
    )

    if not business_type:
        raise HTTPException(
            status_code=400,
            detail="INVALID_BUSINESS_TYPE"
        )


    tenant = Tenant(
        company_name=payload.company_name,
        owner_email=payload.email,
        business_type_id=business_type.id,
        subscription_tier="FREE_TRIAL",
        is_billing_active=True
    )

    print("STEP 3", flush=True)

    db.add(tenant)
    db.commit()

    print("STEP 4", flush=True)
    db.refresh(tenant)


    profile = BusinessProfile(
        business_name=payload.company_name,
        tenant_id=tenant.id,
        business_type_code=business_type.code,
        business_slug=generate_business_slug(
            payload.company_name
        ),
        owner_name=payload.full_name,
        email=payload.email,
        is_public=True
    )

    db.add(profile)
    db.commit()


    assign_features_to_tenant(
        db=db,
        tenant_id=tenant.id,
        business_type_id=business_type.id
    )


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
            start_date=datetime.now(timezone.utc),
            end_date=datetime.now(timezone.utc) + timedelta(days=30),
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
        "trial_days": 30
    }


# ==========================================================================
