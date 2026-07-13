import uuid

from sqlalchemy.orm import Session

from src.models.saas_core import (
    BusinessProfile,
    SocialAccount
)



def create_profile(
    db: Session,
    tenant_id: str,
    data
):

    profile = BusinessProfile(

        id=str(uuid.uuid4()),

        business_name=data.business_name,

        logo_url=data.logo_url,

        phone=data.phone,

        address=data.address,

        description=data.description,

        tenant_id=tenant_id
    )


    db.add(profile)

    db.commit()

    db.refresh(profile)

    return profile




def add_social_account(
    db: Session,
    tenant_id: str,
    data
):

    account = SocialAccount(

        id=str(uuid.uuid4()),

        platform=data.platform,

        account_name=data.account_name,

        account_url=data.account_url,

        status="CONNECTED",

        tenant_id=tenant_id
    )


    db.add(account)

    db.commit()

    db.refresh(account)

    return account



def get_social_accounts(
    db: Session,
    tenant_id: str
):

    return (
        db.query(SocialAccount)
        .filter(
            SocialAccount.tenant_id == tenant_id
        )
        .all()
    )
