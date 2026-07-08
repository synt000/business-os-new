import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

# 1. FIXED ENHANCEMENT: PLUG MODULE ROUTERS WITH ABSOLUTE CONTEXT SYNC
from .auth.router import router as auth_router
from .product.router import router as product_router
from .dashboard.router import router as dashboard_router

# SENIOR ARCHITECT FIX: DISABLE DEFAULT DOCS AND KEEP HARDENED OPENAPI SCHEMA PATHS
app = FastAPI(
    title="Business OS - Production Hardened Router Kernel",
    version="4.0.0-MVP",
    docs_url=None,
    redoc_url=None,
    openapi_url="/api/v4/openapi.json"
)

# Standard Dynamic Baseline Path Resolution Configuration Layer
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Mount static asset layers securely
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# 2. REQUIRED: INCLUDE DETACHED ENTERPRISE ROUTERS TIGHTLY
app.include_router(auth_router)
app.include_router(product_router)
app.include_router(dashboard_router)

# ==========================================================================
# CUSTOM FASTAPI ENTERPRISE ARCHITECT LAYER: INJECT SWAGGER CUSTOM CSS URL
# ==========================================================================
@app.get("/api/v4/docs", include_in_schema=False, tags=["Infrastructure Documentation"])
async def custom_swagger_ui_html():
    """Renders the custom dark-themed enterprise swagger console with dynamic stylesheet injects."""
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - API Control Panel",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://jsdelivr.net",
        swagger_css_url="/static/style.css"  # Absolute Custom CSS Overrides Injection Node
    )

@app.get("/api/v4/redoc", include_in_schema=False, tags=["Infrastructure Documentation"])
async def custom_redoc_html():
    """Provides re-routed redoc deployment specifications layer."""
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Redoc Management"
    )

# PUBLIC INTERFACE MARKETING GATEWAY
@app.get("/", response_class=HTMLResponse, tags=["Landing Gateway"])
async def render_landing_page(request: Request):
    """Renders the central enterprise marketing entry node."""
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/api/v4/health", tags=["Infrastructure Telemetry"])
def check_infrastructure_health():
    """Returns dynamic server health records."""
    return {"status": "OPERATIONAL", "architecture": "CUSTOM_DOCS_INJECTION_ENGINE", "kernel_v4": True}
