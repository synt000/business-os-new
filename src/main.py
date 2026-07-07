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

from src.auth.middleware import AuthMiddleware

# Routers (Standardized to Domain & Core Architecture)
from src.auth.router import router as auth_router
from src.product.router import router as product_router
from src.movement.router import router as movement_router
from src.domains.inventory.router import router as inventory_router
from src.dashboard.router import router as dashboard_router
from src.export.router import router as export_router

app = FastAPI(title="Business OS")

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
app.include_router(inventory_router) # Router internally contains prefix="/inventory"
app.include_router(dashboard_router)
app.include_router(export_router)

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
