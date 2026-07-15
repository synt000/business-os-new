from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user
from src.models.saas_core import User
from src.domains.category.models import Category
from src.domains.category.models import Category

router = APIRouter(
    prefix="/api/v4/business/categories",
    tags=["Category"],
)


@router.get("")
async def list_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rows = (
        db.query(Category)
        .filter(Category.tenant_id == current_user.tenant_id)
        .all()
    )

    return {
        "categories": [
            {
                "id": row.id,
                "name": row.name,
            }
            for row in rows
        ]
    }