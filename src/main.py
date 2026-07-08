import os
from datetime import datetime
from fastapi import FastAPI, Header, HTTPException, status, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

# 1. FIXED ARCHITECTURE: STANDARD PATHWAY IMPORTS (ZERO REDUNDANCY)
from .database import get_db
from .models.saas_core import User, Tenant, SubscriptionTier
from .config.security import get_password_hash

app = FastAPI(
    title="Business OS - Hardened Multi-Tenant Core Kernel",
    version="4.0.0-MVP",
    docs_url="/api/v4/docs"
)

# Standard Dynamic Baseline Path Resolution Configuration Layer
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Mount static asset layers securely
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# Pydantic Inbound Schema Mapped onto Frontend Ingress Tiers
class TenantRegisterInboundSchema(BaseModel):
    company_name: str
    email: EmailStr
    password: str

# PUBLIC LANDING INTERFACE REDIRECTION PATHS
@app.get("/", response_class=HTMLResponse)
async def render_landing_page(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/auth/register", response_class=HTMLResponse)
async def render_register_page(request: Request):
    return templates.TemplateResponse(request=request, name="register.html")

@app.get("/auth/login", response_class=HTMLResponse)
async def render_login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@app.get("/api/v4/health")
def check_infrastructure_health():
    return {"status": "OPERATIONAL"}

# ==========================================================================
# PHASE 1 SOLIDIFIED: REGISTER -> PASSWORD BCRYPT HASH -> REAL DB PIPELINE
# ==========================================================================
@app.post("/api/v4/tenant/onboard", status_code=status.HTTP_201_CREATED)
async def onboard_enterprise_workspace(payload: TenantRegisterInboundSchema, db: Session = Depends(get_db)):
    # 1. Enforce basic string validation boundaries
    if not payload.company_name.strip() or not payload.password.strip():
        raise HTTPException(status_code=422, detail="CRITICAL_FAULT: PARAMETERS_CANNOT_BE_EMPTY")

    # 2. Prevent dynamic user identity overlap leaks cleanly
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="IDENTITY_CLASH: WORK_EMAIL_ALREADY_REGISTERED")

    # 3. Initialize Corporate Tenant Model Structure
    tenant_id = f"tnt_{int(datetime.utcnow().timestamp())}"
    new_tenant = Tenant(
        id=tenant_id,
        company_name=payload.company_name,
        owner_email=payload.email,
        subscription_tier=SubscriptionTier.FREE_TRIAL,
        is_billing_active=True,
        trial_expired=False
    )
    db.add(new_tenant)

    # 4. FIXED COLUMN BOUNDS: SECURE BCRYPT HASHING INSIDE AUTHENTICATED USER MODEL
    user_id = f"usr_{int(datetime.utcnow().timestamp())}"
    encrypted_secure_hash = get_password_hash(payload.password)
    
    new_master_user = User(
        id=user_id,
        email=payload.email,
        hashed_password=encrypted_secure_hash,
        full_name=payload.company_name + " Admin",
        role="ADMIN",
        is_active=True,  # Fully aligned to our unified single table schema bounds
        tenant_id=tenant_id
    )
    db.add(new_master_user)

    # 5. Commit Transaction to app.db Tightly
    try:
        db.commit()
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"DATABASE_TRANSACTION_FAILED: {str(exc)}")

    return {
        "status": "TENANT_SUCCESSFULLY_INITIALIZED",
        "tenant_id": tenant_id,
        "admin_user_id": user_id,
        "trial_tier_active": True
    }
