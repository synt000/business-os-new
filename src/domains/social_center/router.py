from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session


from src.core.database import get_db

from src.core.security import get_current_user

from src.models.saas_core import User


from src.domains.social_center.schemas import (
    BusinessProfileCreate,
    SocialAccountCreate,
    SocialAccountResponse
)


from src.domains.social_center.service import (
    create_profile,
    add_social_account,
    get_social_accounts
)


router = APIRouter(
    prefix="/social",
    tags=["Social Center"]
)



@router.post("/profile")
def profile(
    data: BusinessProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return create_profile(
        db,
        current_user.tenant_id,
        data
    )



@router.post("/accounts")
def account(
    data: SocialAccountCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return add_social_account(
        db,
        current_user.tenant_id,
        data
    )



@router.get(
    "/accounts",
    response_model=list[SocialAccountResponse]
)
def accounts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return get_social_accounts(
        db,
        current_user.tenant_id
    )
