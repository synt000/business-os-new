from fastapi import APIRouter

router = APIRouter(prefix="/audit", tags=["Audit"])

logs = []

@router.get("/")
def get_logs():
    return logs

@router.post("/log")
def create_log(event: str):
    logs.append(event)
    return {"status": "logged"}
