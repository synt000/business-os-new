from pydantic import BaseModel
from typing import Optional


class ProductVariantCreate(BaseModel):
    product_id: str
    variant_name: str
    attributes: Optional[dict] = None


class ProductVariantResponse(ProductVariantCreate):
    id: str
    tenant_id: str

    class Config:
        from_attributes = True


class ProductSKUCreate(BaseModel):
    product_id: str
    variant_id: Optional[str] = None
    sku_code: str
    barcode: Optional[str] = None


class ProductSKUResponse(ProductSKUCreate):
    id: str
    tenant_id: str

    class Config:
        from_attributes = True


class ProductMediaCreate(BaseModel):
    product_id: str
    file_url: str
    media_type: str = "IMAGE"


class ProductMediaResponse(ProductMediaCreate):
    id: str
    tenant_id: str

    class Config:
        from_attributes = True
