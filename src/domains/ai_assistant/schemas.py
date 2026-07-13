from pydantic import BaseModel


class AIChatRequest(BaseModel):
    message: str


class AIChatResponse(BaseModel):
    reply: str
    category: str


class AIInsightResponse(BaseModel):
    title: str
    detail: str
