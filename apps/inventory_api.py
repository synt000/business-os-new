from fastapi import APIRouter, Depends
from infrastructure.db.session import get_db
from core.rbac import RoleChecker
from services.inventory_service import InventoryService

router = APIRouter(prefix="/inventory")

@router.post("/add")
def add_stock(
    product_id: str,
    quantity: float,
    db=Depends(get_db),
    user=Depends(RoleChecker(["admin", "staff"]))
):
    return InventoryService.add_stock(
        db,
        product_id,
        quantity,
        user["tenant_id"]
    )


@router.post("/remove")
def remove_stock(
    product_id: str,
    quantity: float,
    db=Depends(get_db),
    user=Depends(RoleChecker(["admin", "staff"]))
):
    return InventoryService.remove_stock(
        db,
        product_id,
        quantity,
        user["tenant_id"]
    )


@router.get("/history")
def history(
    product_id: str,
    db=Depends(get_db),
    user=Depends(RoleChecker(["admin", "staff"]))
):
    return InventoryService.history(
        db,
        product_id,
        user["tenant_id"]
    )
