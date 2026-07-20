from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session


from src.core.database import get_db

from src.core.security import get_current_user

from src.models.saas_core import User


from src.domains.social_center.schemas import (
    BusinessProfileCreate,
    SocialAccountCreate,
    SocialAccountResponse,
    SocialLeadResponse,
    SocialLeadStatusUpdate
)


from src.domains.social_center.service import (
    create_profile,
    add_social_account,
    get_social_accounts,
    get_social_leads,
    update_social_lead_status
)


router = APIRouter(
    prefix="/social",
    tags=["Social Center"]
)


templates = Jinja2Templates(
    directory="src/templates"
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


from src.domains.social_center.service import get_social_messages
from src.domains.social_center.schemas import SocialMessageResponse


@router.get(
    "/messages",
    response_model=list[SocialMessageResponse]
)
def messages(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_social_messages(
        db,
        current_user.tenant_id
    )

# ======================================
# SOCIAL DASHBOARD SUMMARY
# ======================================

from src.domains.social_center.service import get_social_summary


@router.get("/summary")
def summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_social_summary(
        db,
        current_user.tenant_id
    )



# ======================================
# SOCIAL LEADS
# ======================================

@router.get(
    "/leads",
    response_model=list[SocialLeadResponse]
)
def leads(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_social_leads(
        db,
        current_user.tenant_id
    )


# ======================================
# UPDATE SOCIAL LEAD STATUS
# ======================================

@router.patch(
    "/leads/{lead_id}/status",
    response_model=SocialLeadResponse
)
def update_lead_status(
    lead_id: str,
    data: SocialLeadStatusUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return update_social_lead_status(
        db,
        current_user.tenant_id,
        lead_id,
        data.status
    )


# ======================================
# SOCIAL CENTER UI
# ======================================

@router.get(
    "/ui",
    response_class=HTMLResponse,
    include_in_schema=False
)
def social_center_ui(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="social_center.html"
    )

# =====================================
# SOCIAL CENTER UI
# =====================================

import os

from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


BASE_DIR=os.path.dirname(
os.path.dirname(
os.path.dirname(
os.path.abspath(__file__)
)))

templates=Jinja2Templates(
directory=os.path.join(
BASE_DIR,
"templates"
)
)


@router.get(
"/ui",
response_class=HTMLResponse,
include_in_schema=False
)
async def social_center_ui(
request:Request
):
    return templates.TemplateResponse(
        request=request,
        name="social_center.html"
    )

