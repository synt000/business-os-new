import os
from datetime import datetime
from fastapi import FastAPI, Header, HTTPException, status, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

# Hardened System Layer Architecture Context Mappings
from .database import get_db
from .models.saas_core import User, Tenant, SubscriptionTier
from .config.security import get_password_hash, verify_password, create_access_token, create_refresh_token
from .config.dependencies import get_current_user

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

# Pydantic Schemas Bound onto Ingress Tiers
class TenantRegisterInboundSchema(BaseModel):
    company_name: str
    email: EmailStr
    password: str

class UserLoginInboundSchema(BaseModel):
    email: EmailStr
    password: str

# PUBLIC LANDING PAGES REDIRECTION GATEWAYS
@app.get("/", response_class=HTMLResponse)
async def render_landing_page(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/auth/register", response_class=HTMLResponse)
async def render_register_page(request: Request):
    return templates.TemplateResponse(request=request, name="register.html")

@app.get("/auth/login", response_class=HTMLResponse)
async def render_login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@app.get("/dashboard", response_class=HTMLResponse)
async def render_secure_workspace_dashboard(request: Request):
    return templates.TemplateResponse(request=request, name="workspace.html")

@app.get("/api/v4/health")
def check_infrastructure_health():
    return {"status": "OPERATIONAL"}

# ==========================================================================
# PHASE 1 PIPELINE: ACCOUNT ONBOARDING RESILIENCE
# ==========================================================================
@app.post("/api/v4/tenant/onboard", status_code=status.HTTP_201_CREATED)
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

# ==========================================================================
# PHASE 1 & 2 SECURE ENDPOINT: VERIFY BCRYPT & GENERATE TOKENS
# ==========================================================================
@app.post("/api/v4/auth/login")
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
    refresh_token = create_refresh_token(data=token_claims)

    return {
        "token_type": "bearer",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "tenant_id": target_user.tenant_id,
        "role": target_user.role
    }

# ==========================================================================
# PHASE 2 PROTECTED CORE SEGMENTS: MULTI-TENANT ISOLATED ENDPOINTS
# ==========================================================================
@app.get("/api/v4/dashboard/analytics", tags=["Guarded Business API Engine"])
async def get_isolated_analytics_summary(current_user: User = Depends(get_current_user)):
    return {
        "context_scope": "TENANT_ISOLATED_DATA_GRID",
        "tenant_id": current_user.tenant_id,
        "authorized_user_id": current_user.id,
        "role_signature": current_user.role,
        "metrics_summary": {
            "total_sales_volume_usd": 142384.50,
            "processed_transaction_count": 8492,
            "active_skus_count": 1248
        }
    }

@app.get("/api/v4/inventory/items", tags=["Guarded Business API Engine"])
async def get_isolated_inventory_ledger(current_user: User = Depends(get_current_user)):
    return {
        "tenant_id": current_user.tenant_id,
        "module": "INVENTORY",
        "storage_shards": ["Warehouse-A", "Warehouse-Central"],
        "items": [
            {"sku": "SKU-1248", "name": "Enterprise Core Shard", "qty": 850, "status": "STABLE"},
            {"sku": "SKU-8492", "name": "Distributed Module Node", "qty": 398, "status": "OPTIMAL"}
        ]
    }

@app.get("/api/v4/orders/processed", tags=["Guarded Business API Engine"])
async def get_isolated_orders_stream(current_user: User = Depends(get_current_user)):
    return {
        "tenant_id": current_user.tenant_id,
        "module": "SALES_PIPELINE",
        "recent_streams_count": 8492,
        "status": "OPERATIONAL"
    }

@app.get("/api/v4/reports/financial", tags=["Guarded Business API Engine"])
async def get_isolated_financial_report(current_user: User = Depends(get_current_user)):
    if current_user.role not in ["ADMIN", "MANAGER"]:
        raise HTTPException(status_code=403, detail="ACCESS_DENIED: INSUFFICIENT_ROLE_PRIVILEGES")
    return {
        "tenant_id": current_user.tenant_id,
        "module": "CORE_ACCOUNTING",
        "gross_volume_usd": 14200000.00,
        "audit_compliance": True
    }
