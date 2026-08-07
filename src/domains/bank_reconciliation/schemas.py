from datetime import datetime
from pydantic import BaseModel


class BankTransactionCreate(BaseModel):

    bank_name: str
    account_number: str | None = None
    transaction_date: datetime
    external_reference: str | None = None
    description: str | None = None
    amount: float
    direction: str
