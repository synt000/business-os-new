from pydantic import BaseModel


class PurchaseItemCreate(BaseModel):
    product_id: str
    quantity: int
    unit_cost: float


class PurchaseCreate(BaseModel):
    purchase_number: str
    supplier_id: str
    items: list[PurchaseItemCreate]


class PurchaseResponse(BaseModel):
    id: str
    purchase_number: str
    supplier_id: str
    total_amount: float
    status: str

    class Config:
        from_attributes = True
