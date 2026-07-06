from fastapi import APIRouter
from core.db import SessionLocal
from core.models import EmailLog

router = APIRouter()

@router.get("/emails")
def get_emails():
    db = SessionLocal()
    logs = db.query(EmailLog).all()
    return logs
