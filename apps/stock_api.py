from fastapi import APIRouter, Depends
from infrastructure.db.session import get_db
from core.rbac import RoleChecker
from services.stock_service import StockService

router = APIRouter(prefix="/stock")

@router.get("/{product_id}")
def get_stock(product_id: str, db=Depends(get_db), user=Depends(RoleChecker(["admin","staff"]))):
    return StockService.get_stock(db, product_id, user["tenant_id"])
