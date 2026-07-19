from pydantic import BaseModel
from datetime import datetime


class AIInsightResponse(BaseModel):
    id: str
    title: str
    message: str
    priority: str
    created_at: datetime

    class Config:
        from_attributes = True


class AIInsightCreate(BaseModel):
    title: str
    message: str
    priority: str = "NORMAL"
