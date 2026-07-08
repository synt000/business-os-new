import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# 1. FIXED ENHANCEMENT: PLUG MODULE ROUTERS WITH ABSOLUTE CONTEXT SYNC
from .auth.router import router as auth_router
from .product.router import router as product_router
from .dashboard.router import router as dashboard_router

# PRODUCTION FIXED: HARDENED SPECIFICATIONS MATCHING SWAGGER/OPENAPI CHANNELS
app = FastAPI(
    title="Business OS - Production Hardened Router Kernel",
    version="4.0.0-MVP",
    docs_url="/api/v4/docs",
    openapi_url="/api/v4/openapi.json",
    redoc_url="/api/v4/redoc"
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

# PUBLIC INTERFACE MARKETING GATEWAY
@app.get("/", response_class=HTMLResponse, tags=["Landing Gateway"])
async def render_landing_page(request: Request):
    """Renders the central enterprise marketing entry node."""
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/api/v4/health", tags=["Infrastructure Telemetry"])
def check_infrastructure_health():
    """Returns dynamic server health records."""
    return {"status": "OPERATIONAL", "architecture": "ROUTER_BASED_STANDALONE", "kernel_v4": True}
