from pydantic import BaseModel

class ProductCreateSchema(BaseModel):
    name: str
    price: float
    category_id: str


class CategoryCreateSchema(BaseModel):
    name: str
    description: str | None = None


class InventorySchema(BaseModel):
    product_id: str
    quantity: float
