from fastapi import APIRouter
from datetime import datetime, timedelta

router = APIRouter(prefix="/trial", tags=["Trial"])

@router.get("/start")
def start_trial():
    return {
        "trial_start": str(datetime.utcnow()),
        "trial_end": str(datetime.utcnow() + timedelta(days=7))
    }
