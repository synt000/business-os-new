from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    sku: str
    price: int
    purchase_price: int = 0
    retail_price: int = 0
    barcode: str | None = None
    reorder_level: int = 5
    category_id: str | None = None
    description: str | None = None
    brand: str | None = None
    image_url: str | None = None


class ProductResponse(BaseModel):
    id: str
    name: str
    sku: str
    price: int
    description: str | None = None
    brand: str | None = None
    image_url: str | None = None

    class Config:
        from_attributes = True
