from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user

from src.models.saas_core import User

from src.domains.purchase.schemas import (
    PurchaseCreate,
    PurchaseResponse,
)

from src.domains.purchase.services.purchase_service import (
    create_purchase,
)


router = APIRouter(
    prefix="/purchases",
    tags=["Purchases"]
)



@router.post(
    "/",
    response_model=PurchaseResponse
)
async def create_purchase_api(
    data: PurchaseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    try:

        return create_purchase(
            db,
            current_user.tenant_id,
            data
        )

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
