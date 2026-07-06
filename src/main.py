from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from infrastructure.db.base import Base
from infrastructure.db.session import engine
from src.auth.router import router as auth_router
from src.product.router import router as product_router
from src.category.router import router as category_router
from src.movement.router import router as movement_router
from src.inventory.router import router as inventory_router
from src.dashboard.router import router as dashboard_router
from src.export.router import router as export_router
from src.auth.middleware import AuthMiddleware

app = FastAPI(title="Business OS")

# Template setting
templates = Jinja2Templates(directory="src/templates")

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)

app.add_middleware(AuthMiddleware)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

app.include_router(auth_router)
app.include_router(product_router)
app.include_router(category_router)
app.include_router(movement_router)
app.include_router(inventory_router)
app.include_router(dashboard_router)
app.include_router(export_router)
