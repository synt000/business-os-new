from fastapi import FastAPI

from apps.email_api import router as email_router
from apps.health_api import router as health_router
from apps.dashboard.api import router as dashboard_router

app = FastAPI(title="Business OS")

app.include_router(email_router)
app.include_router(health_router)
app.include_router(dashboard_router)
