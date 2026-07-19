from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user

from src.models.saas_core import User

from src.domains.trial.service import (
    get_trial_status
)


router = APIRouter(
    prefix="/trial",
    tags=["Trial"]
)


@router.get("/status")
def trial_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return get_trial_status(
        db=db,
        tenant_id=current_user.tenant_id
    )
