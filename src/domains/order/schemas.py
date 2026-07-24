from pydantic import BaseModel


class OrderItemCreate(BaseModel):
    product_id: str
    quantity: int
    price: float


class OrderCreate(BaseModel):
    order_number: str
    customer_id: str
    customer_name: str
    customer_phone: str | None = None
    items: list[OrderItemCreate]


class OrderResponse(BaseModel):
    id: str
    order_number: str
    total_amount: float
    order_status: str

    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    status: str
