import os

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.database import engine, Base

from src.domains.tenant.models import Tenant
from src.domains.user.models import User
from src.domains.category.models import Category
from src.domains.product.models import Product
from src.domains.inventory.models import Inventory
from src.domains.movement.models import StockMovement
from src.domains.order.models import Order, OrderItem
from src.domains.audit.models import AuditLog

from src.database_mega_upgrade import (
    SocialWebhookLog,
    TenantPartnership,
    PredictiveAnalytic,
    FranchiseNetwork,
)

from src.auth.middleware import AuthMiddleware

from src.auth.router import router as auth_router
from src.product.router import router as product_router
from src.movement.router import router as movement_router
from src.domains.inventory.router import router as inventory_router
from src.dashboard.router import router as dashboard_router
from src.export.router import router as export_router
from src.domains.social.router import router as social_router
from src.domains.partnership.router import router as partnership_router
from src.domains.analytics.router import router as analytics_router
from src.domains.franchise.router import router as franchise_router

app = FastAPI(title="Business OS - Mega SaaS ERP")

app.add_middleware(AuthMiddleware)


@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(CURRENT_DIR, "static")
TEMPLATES_DIR = os.path.join(CURRENT_DIR, "templates")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

templates = Jinja2Templates(directory=TEMPLATES_DIR)

app.include_router(auth_router, prefix="/auth")
app.include_router(product_router)
app.include_router(movement_router)
app.include_router(inventory_router)
app.include_router(dashboard_router)
app.include_router(export_router)
app.include_router(social_router)
app.include_router(partnership_router)
app.include_router(analytics_router)
app.include_router(franchise_router)
@app.get("/health")
async def health():
    return {"status": "ok"}


# -----------------------------
# WEB UI ROUTES
# -----------------------------

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={},
    )


@app.get("/auth/login", response_class=HTMLResponse)
async def login_ui(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={},
    )


@app.get("/auth/register", response_class=HTMLResponse)
async def register_ui(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={},
    )


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_ui(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={},
    )


@app.get("/products/ui", response_class=HTMLResponse)
async def products_ui(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="products.html",
        context={},
    )


@app.get("/inventory/ui", response_class=HTMLResponse)
async def inventory_ui(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="inventory.html",
        context={},
    )


@app.get("/movements/ui", response_class=HTMLResponse)
async def movements_ui(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="movements.html",
        context={},
    )


@app.get("/orders/ui", response_class=HTMLResponse)
async def orders_ui(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="orders.html",
        context={},
    )
