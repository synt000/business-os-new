from fastapi import FastAPI

from core.telemetry import telemetry_middleware
from core.metrics_middleware import metrics_middleware
from core.error_handler import global_exception_handler

from apps.category_api import router as category_router
from apps.product_api import router as product_router
from apps.inventory_api import router as inventory_router
from apps.metrics_api import router as metrics_router

app = FastAPI(title="Business OS API")

# 🔥 Observability stack (order matters)
app.middleware("http")(metrics_middleware)
app.middleware("http")(telemetry_middleware)

# Routers
app.include_router(category_router)
app.include_router(product_router)
app.include_router(inventory_router)
app.include_router(metrics_router)

# Global error handler
app.add_exception_handler(Exception, global_exception_handler)


@app.get("/health")
def health():
    return {"status": "ok"}
