from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.auth.dependencies import get_current_user
from src.domains.trial.guard import require_active_subscription

from src.domains.product.services.product_service import get_products


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get("")
def list_products(
    db: Session = Depends(get_db),
    current_user = Depends(require_active_subscription)
):
    return get_products(
        db=db,
        tenant_id=current_user.tenant_id
    )
