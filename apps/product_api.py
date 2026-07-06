from fastapi import APIRouter, Depends
from infrastructure.db.session import get_db
from core.rbac import RoleChecker
from services.product_service import ProductService

router = APIRouter(prefix="/products")

@router.post("/")
def create_product(
    name: str,
    price: float,
    category_id: str,
    db=Depends(get_db),
    user=Depends(RoleChecker(["admin", "staff"]))
):
    return ProductService.create(
        db,
        name,
        price,
        category_id,
        user["tenant_id"]
    )


@router.get("/")
def list_products(
    db=Depends(get_db),
    user=Depends(RoleChecker(["admin", "staff"]))
):
    return ProductService.list(db, user["tenant_id"])
