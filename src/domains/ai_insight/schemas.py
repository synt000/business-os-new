from pydantic import BaseModel


class AIInsightResponse(BaseModel):

    title: str
    message: str
    level: str

    class Config:
        from_attributes = True
