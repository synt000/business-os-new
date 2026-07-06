from fastapi import APIRouter
from core.task_store import get_task

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/task/{task_id}")
def get_task_status(task_id: str):
    data = get_task(task_id)

    return {
        "task_id": task_id,
        "status": data.get("status"),
        "to": data.get("to"),
        "subject": data.get("subject")
    }
