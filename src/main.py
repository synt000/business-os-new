from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.core.config import settings
from src.core.middlewares import SecurityInfrastructureMiddleware, setup_global_exception_handlers
from src.auth.router import router as auth_router
from src.product.router import router as product_router
from src.dashboard.router import router as dashboard_router

# ==========================================================================
# 1. CORE TELEMETRY TRACKER: VERIFY JWT CRYPTOGRAPHIC SECRET KEY LOAD STAGE
# ==========================================================================
print(f"📡 [DevOps Telemetry] Loaded Cryptographic Secret Prefix: {settings.SECRET_KEY[:10]}")

app = FastAPI(


    title="Business OS - မြန်မာလုပ်ငန်းသုံး စနစ်တော်ကြီး (v5.5)",
    description="Monolithic B2B SaaS Enterprise Engine Matrix with Enhanced Protection Layers",
    version="5.5.0-Enterprise",
    docs_url="/api/v4/docs",  # Fully standard local compliance asset mapping natively
    redoc_url=None,
    openapi_url="/api/v4/openapi.json"
)
app.mount("/static", StaticFiles(directory="src/static"), name="static")


# REGISTER GLOBAL Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SecurityInfrastructureMiddleware)

# INITIALIZE EXCEPTIONS CONTROL PIPELINES
setup_global_exception_handlers(app)

# ==========================================================================
# 2. AUDIT TESTING ENDPOINTS: SYSTEM CONFIGURATION INSIGHT PIPELINES
# ==========================================================================
@app.get("/config", include_in_schema=False)
@app.get("/api/v4/config", tags=["Infrastructure Telemetry"])
def get_system_runtime_configuration_matrix():
    """Provides authoritative immutable metadata diagnostics to verify configuration sync states."""
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.API_VERSION_PREFIX,
        "rate_limiting_cap": settings.RATE_LIMIT_PER_MINUTE,
        "token_compliance": {
            "issuer_id": settings.TOKEN_ISSUER,
            "audience_id": settings.TOKEN_AUDIENCE
        }
    }

# ATTACH UNIFIED SYSTEM DOMAINS ROUTERS
app.include_router(auth_router)
app.include_router(product_router)
app.include_router(dashboard_router)

from fastapi.responses import RedirectResponse

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/dashboard")

