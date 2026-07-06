from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from infrastructure.db.session import get_db
from services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/summary")
def get_dashboard_summary(request: Request, db: Session = Depends(get_db)):
    return DashboardService.get_summary(db, request.state.tenant_id)
