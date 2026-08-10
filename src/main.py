from src.telegram_bot.webhook import router as telegram_router

# ===== DOMAIN MODEL REGISTRY LOAD =====
# import src.domains.product.models
# import src.domains.inventory.models
# import src.domains.purchase.models
# import src.domains.accounting.models

import os
from dotenv import load_dotenv

load_dotenv('.env')

# ==========================================================================
# ATOMIC ZERO-TOUCH DATABASE MAPPER COMPILATION SHIELD
# ==========================================================================
try:
    import importlib
    from sqlalchemy.orm import configure_mappers, relationship
    
    # ၁။ မော်ဒယ်ဖိုင်တွဲများအားလုံးကို အတင်းအကျပ် ရှာဖွေဆွဲတင်ခြင်း
    importlib.import_module("src.models.saas_core")
    try:
        importlib.import_module("src.models.inventory_models")
    except Exception:
        pass
        
    from src.models import saas_core
    
    Category = getattr(saas_core, 'Category', None)
    if not Category and hasattr(saas_core, 'inventory_models'):
        Category = getattr(saas_core.inventory_models, 'Category', None)
        
    Tenant = getattr(saas_core, 'Tenant', None)
    
    # ၂။ ဇယားနှစ်ခုလုံး၏ Properties များကို အပြန်အလှန် (Atomic နှစ်ဖက်လုံး) တပြိုင်နက်တည်း ထိုးသွင်းကုသခြင်း
    if Category and Tenant:
        Category.tenant = relationship("Tenant", back_populates="categories")
        Tenant.categories = relationship("Category", back_populates="tenant")
        
        # ၃။ SQL Alchemy Mapper တစ်ခုလုံးကို အပြတ် ရှင်းလင်းတည်ဆောက်ခြင်း
        configure_mappers()
        print("[✓] ATOMIC SHIELD: SQL Alchemy Model Mapping Synchronized Perfectly.")
except Exception as e:
    pass
# ==========================================================================

from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html

from src.core.config import settings
from src.core.middlewares import SecurityInfrastructureMiddleware, setup_global_exception_handlers
from src.auth.router import router as auth_router
from src.auth.two_factor import router as two_factor_router
from src.auth.session_router import router as session_router
from src.auth.refresh_router import router as refresh_router
from src.product.router import router as product_router
from src.movement.router import router as movement_router
from src.domains.social.router import router as social_webhook_router
from src.domains.social_center.router import router as social_center_router
from src.domains.social_post.router import router as social_post_router
from src.domains.campaign.router import router as campaign_router
from src.domains.campaign.services.scheduler_service import (
    start_scheduler,
    scheduler,
)
from src.domains.campaign.execution_models import CampaignExecutionLog
from src.core.database import SessionLocal
from src.domains.social_center.ui_router import router as social_center_ui_router
from src.domains.social_center.ui_router import router as social_ui_router
from src.domains.dashboard.router import router as dashboard_router
from src.dashboard.router import router as ui_dashboard_router
from src.domains.platform.router import router as platform_router
from src.public_router import router as public_router
from src.public_page_router import router as public_page_router
from src.domains.welcome.admin_router import router as welcome_admin_router
from src.business_settings_router import router as business_settings_router
from src.domains.category.router import router as category_router
from src.domains.tenant.router import router as tenant_router
from src.domains.guest_workspace.router import router as guest_workspace_router
from src.domains.welcome.router import router as welcome_router
from src.domains.inventory.router import router as inventory_router
from src.domains.order.router import router as order_router
from src.domains.customer.router import router as customer_router
from src.domains.supplier.router import router as supplier_router
from src.domains.supplier_payment.router import router as supplier_payment_router
from src.domains.customer_payment.router import router as customer_payment_router
from src.domains.purchase.router import router as purchase_router
from src.domains.invoice.router import router as invoice_router
from src.domains.receivable.router import router as receivable_router
from src.domains.payment.router import router as payment_router
from src.domains.bank_reconciliation.router import router as bank_reconciliation_router
from src.domains.payment.webhook.router import router as payment_webhook_router
from src.domains.customer_finance.router import router as customer_finance_router
from src.domains.finance.router import router as finance_router
from src.domains.accounting.router import router as accounting_router

from src.business_profile_router import router as business_profile_router
from src.domains.subscription.router import router as subscription_router
from src.domains.trial.router import router as trial_router
from src.domains.admin.router import router as admin_router
from src.domains.permissions.router import router as permissions_router
from src.domains.rental.router import router as rental_router
from src.domains.ai_insight.router import router as ai_insight_router
from src.domains.ai_insight.dashboard_router import router as ai_dashboard_router
from src.domains.ai_assistant.router import router as ai_assistant_router
from src.domains.analytics.router import router as analytics_router
from src.domains.device.router import router as device_router
from src.security_center.router import router as security_center_router
from src.domains.audit.router import router as audit_router
from src.domains.license.router import router as license_router
from src.domains.payment_gateway.router import router as payment_gateway_router

from src.feedback.router import router as feedback_router

print("📡 [DevOps Telemetry] Cryptographic Secret Loaded")

app = FastAPI(
    title="Business OS - မြန်မာလုပ်ငန်းသုံး စနစ်တော်ကြီး (v5.5)",
    description="Hybrid B2B SaaS Monolithic Enterprise Architecture Network",
    version="5.5.0-Enterprise",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/api/v4/openapi.json"
)


@app.on_event("startup")
def startup_scheduler():
    start_scheduler()

@app.get("/health")
def system_health():
    scheduler_jobs = scheduler.get_jobs() if scheduler.running else []

    db = SessionLocal()
    try:
        pending_retries = (
            db.query(CampaignExecutionLog)
            .filter(
                CampaignExecutionLog.status == "failed",
                CampaignExecutionLog.retry_count < CampaignExecutionLog.max_retries,
            )
            .count()
        )

        permanent_failures = (
            db.query(CampaignExecutionLog)
            .filter(
                CampaignExecutionLog.status == "failed_permanent",
            )
            .count()
        )
    finally:
        db.close()

    return {
        "status": "ok",
        "service": "business-os",
        "version": "5.5.0-Enterprise",
        "scheduler": {
            "running": scheduler.running,
            "jobs": len(scheduler_jobs),
            "job_ids": [job.id for job in scheduler_jobs],
        },
        "campaign_execution": {
            "pending_retries": pending_retries,
            "permanent_failures": permanent_failures,
        },
    }

from fastapi.responses import JSONResponse
# REGISTER GLOBAL MIDDLEWARES
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SecurityInfrastructureMiddleware)

# INITIALIZE CENTRALIZED EXCEPTIONS CONTROL
setup_global_exception_handlers(app)

# ==========================================================================
# 1. ENFORCE STATIC ASSETS MOUNTING LAYER (100% BLANK-PROOF IMMUTABLE)
# ==========================================================================
static_directory_path = "src/static"
if os.path.exists(static_directory_path):
    app.mount("/static", StaticFiles(directory=static_directory_path), name="static")
    print(f"✅ [UI Sync] Preexisting Frontend Static Assets Mounted Safely from {static_directory_path}")

# ==========================================================================
# 2. AUTOMATED BACKWARD COMPATIBILITY: FRONTEND HTML INLINE PAGES DIRECTORS
# ==========================================================================

# AUTH ROUTER FASTAPI COMPATIBILITY FIX
# Manually attach routes because include_router() is currently
# producing _IncludedRouter placeholders in this project.
for _auth_route in auth_router.routes:
    app.router.routes.append(_auth_route)

app.include_router(two_factor_router)
app.include_router(session_router)
app.include_router(refresh_router)
# PRODUCT ROUTER FASTAPI 0.139 COMPATIBILITY FIX
for _product_route in product_router.routes:
    app.router.routes.append(_product_route)
app.include_router(movement_router)
app.include_router(category_router)
app.include_router(tenant_router)
app.include_router(guest_workspace_router)
app.include_router(welcome_router)
app.include_router(subscription_router)
app.include_router(trial_router)
app.include_router(inventory_router)

# ORDER ROUTER FASTAPI 0.139 COMPATIBILITY FIX
for _order_route in order_router.routes:
    app.router.routes.append(_order_route)


app.include_router(customer_router)
app.include_router(supplier_router)
app.include_router(supplier_payment_router)
app.include_router(customer_payment_router)
app.include_router(purchase_router)
app.include_router(invoice_router)
app.include_router(receivable_router)
# OLD PAYMENT INCLUDE REMOVED
app.include_router(payment_router)
for _bank_route in bank_reconciliation_router.routes:
    app.router.routes.append(_bank_route)
app.include_router(payment_webhook_router)
app.include_router(customer_finance_router)
app.include_router(finance_router)
app.include_router(accounting_router)
app.include_router(public_router)
app.include_router(business_settings_router)
app.include_router(business_profile_router)
app.include_router(admin_router)
app.include_router(permissions_router)
app.include_router(rental_router)
app.include_router(platform_router)
app.include_router(ai_insight_router)
app.include_router(ai_dashboard_router)
app.include_router(ai_assistant_router)

app.include_router(analytics_router)

app.include_router(license_router)
app.include_router(device_router)
app.include_router(security_center_router)
app.include_router(audit_router)
app.include_router(payment_gateway_router)
app.include_router(social_center_router)
app.include_router(social_center_ui_router)
app.include_router(social_post_router)
app.include_router(campaign_router)


# ==========================================
# PHASE 6.1-E OWNER DASHBOARD MANUAL ATTACH
# ==========================================
from fastapi.routing import APIRoute

for _owner_route in dashboard_router.routes:
    if isinstance(_owner_route, APIRoute):
        _owner_route.path = "/api/v4" + _owner_route.path

    app.router.routes.append(_owner_route)

# ================================
# UI DASHBOARD ROUTER MANUAL ATTACH
# ================================
for _ui_route in ui_dashboard_router.routes:
    app.router.routes.append(_ui_route)



app.include_router(feedback_router)

app.include_router(public_page_router)
app.include_router(welcome_admin_router)

from src.domains.website_settings.router import router as website_settings_router
app.include_router(website_settings_router)

# =====================================================
@app.get("/api/v4/docs", include_in_schema=False)
async def custom_swagger_ui_portal_ingress():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="Business OS - လုပ်ငန်းသုံး APIs ပေါ်တယ်လ်",
        swagger_js_url="https://cloudflare.com",
        swagger_css_url="https://cloudflare.com"
    )

@app.get("/config", include_in_schema=False)
@app.get("/api/v4/config", tags=["Infrastructure Telemetry"])
def get_system_runtime_configuration_matrix():
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.API_VERSION_PREFIX
    }
from fastapi.responses import Response

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

# Social Commerce Webhook
app.include_router(social_webhook_router)


## =====================================================
## FASTAPI 0.118+ INCLUDED ROUTER EXPANSION FIX
## =====================================================
#
#
# =====================================================
# INCLUDED ROUTER EXPANSION DISABLED
# =====================================================


# Telegram CEO Bot Webhook
app.include_router(telegram_router)

# =====================================================


# ==============================
# Social Center Router
# ==============================
