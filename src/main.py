import os
from fastapi import FastAPI, Header, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

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

# Mock Database Persistence Dictionaries
TENANTS_DB = {}

# Pydantic Model Schema Bound to Frontend Request Bodies
class TenantOnboardInboundSchema(BaseModel):
    id: str
    company_name: str
    email: str

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

# PRODUCTION FIXED: HARMONIZED POST ROUTE WITH PURE JSON BODY INGESTION
@app.post("/api/v4/tenant/onboard", status_code=status.HTTP_201_CREATED)
async def onboard_enterprise_workspace(payload: TenantOnboardInboundSchema):
    # Enforce basic metadata boundary validations
    if not payload.company_name.strip() or not payload.email.strip():
        raise HTTPException(status_code=422, detail="CRITICAL_FAULT: PARAMETERS_CANNOT_BE_EMPTY")

    # Prevent dynamic registration identity overlap leaks
    if payload.id in TENANTS_DB:
        raise HTTPException(status_code=400, detail="IDENTITY_CLASH: TENANT_ID_ALREADY_EXISTS")

    # Save cleanly to persistent storage maps
    TENANTS_DB[payload.id] = {
        "company_name": payload.company_name,
        "email": payload.email,
        "subscription_tier": "FREE_TRIAL"
    }
        
    return {"status": "TENANT_SUCCESSFULLY_INITIALIZED", "tenant_id": payload.id, "trial_tier_active": True}
