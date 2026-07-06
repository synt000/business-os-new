from fastapi import APIRouter, Depends
from infrastructure.db.session import get_db
from core.rbac import RoleChecker
from services.category_service import CategoryService

router = APIRouter(prefix="/categories")

@router.post("/")
def create_category(
    name: str,
    description: str = "",
    db=Depends(get_db),
    user=Depends(RoleChecker(["admin", "staff"]))
):
    return CategoryService.create(
        db,
        name,
        description,
        user["tenant_id"]
    )


@router.get("/")
def list_categories(
    db=Depends(get_db),
    user=Depends(RoleChecker(["admin", "staff"]))
):
    return CategoryService.list(db, user["tenant_id"])
