from pydantic import BaseModel
from uuid import UUID


class OrderItemCreate(BaseModel):
    product_id: UUID
    quantity: int
    price: float


class OrderCreate(BaseModel):
    order_number: str
    items: list[OrderItemCreate]


class OrderResponse(BaseModel):
    id: str
    order_number: str
    total_amount: float
    order_status: str

    class Config:
        from_attributes = True


from pydantic import BaseModel


class OrderStatusUpdate(BaseModel):
    status: str
