from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Database & Models (Registry)
from src.database import engine, Base
from src.domains.tenant.models import Tenant
from src.domains.user.models import User
from src.domains.category.models import Category
from src.domains.product.models import Product
from src.domains.inventory.models import Inventory
from src.domains.movement.models import StockMovement
from src.domains.order.models import Order, OrderItem
from src.domains.audit.models import AuditLog

# Import Mega Upgrade Tables to register inside metadata
from src.database_mega_upgrade import SocialWebhookLog, TenantPartnership, PredictiveAnalytic, FranchiseNetwork

from src.auth.middleware import AuthMiddleware

# Routers (Standardized to Domain & Core Architecture)
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

app.mount("/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory="src/templates")

# Router Registrations
app.include_router(auth_router)
app.include_router(product_router)
app.include_router(movement_router)
app.include_router(inventory_router)
app.include_router(dashboard_router)
app.include_router(export_router)
app.include_router(social_router)
app.include_router(partnership_router)
app.include_router(analytics_router)
app.include_router(franchise_router) # Integrated Franchise Multi-Branch Router

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
