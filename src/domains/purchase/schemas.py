from pydantic import BaseModel


class PurchaseCreate(BaseModel):
    procurement_number: str
    supplier_id: str
    product_id: str
    qty_purchased: int
    unit_cost: float


class PurchaseResponse(BaseModel):
    id: str
    procurement_number: str
    supplier_id: str
    product_id: str
    qty_purchased: int
    unit_cost: float
    total_cost: float

    class Config:
        from_attributes = True
