from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user

from src.models.saas_core import User
from src.domains.platform.service import get_platform_dashboard

router = APIRouter(
    prefix="/platform",
    tags=["Platform Owner"]
)


@router.get("/dashboard")
def platform_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return {
        "status": "SUCCESS",
        "owner": current_user.email,
        "dashboard": get_platform_dashboard(db)
    }
