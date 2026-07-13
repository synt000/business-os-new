from pydantic import BaseModel
from datetime import datetime


class LedgerItem(BaseModel):
    entry_type: str
    account_head: str
    amount: float
    reference_id: str | None = None
    description: str | None = None
    created_at: datetime


class LedgerResponse(BaseModel):
    status: str
    total: int
    items: list[LedgerItem]
