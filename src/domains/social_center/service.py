import uuid

from sqlalchemy.orm import Session

from src.models.saas_core import (
    BusinessProfile,
    SocialAccount,
    SocialMessage
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


# ======================================
# SOCIAL DASHBOARD SUMMARY
# ======================================

from sqlalchemy import func


def get_social_summary(
    db: Session,
    tenant_id: str
):

    total_accounts = (
        db.query(SocialAccount)
        .filter(
            SocialAccount.tenant_id == tenant_id
        )
        .count()
    )


    connected_accounts = (
        db.query(SocialAccount)
        .filter(
            SocialAccount.tenant_id == tenant_id,
            SocialAccount.status == "CONNECTED"
        )
        .count()
    )


    total_messages = (
        db.query(SocialMessage)
        .filter(
            SocialMessage.tenant_id == tenant_id
        )
        .count()
    )


    unread_messages = (
        db.query(SocialMessage)
        .filter(
            SocialMessage.tenant_id == tenant_id,
            SocialMessage.status == "NEW"
        )
        .count()
    )


    platforms = (
        db.query(
            SocialMessage.platform,
            func.count(SocialMessage.id)
        )
        .filter(
            SocialMessage.tenant_id == tenant_id
        )
        .group_by(
            SocialMessage.platform
        )
        .all()
    )


    return {
        "total_accounts": total_accounts,
        "connected_accounts": connected_accounts,
        "total_messages": total_messages,
        "unread_messages": unread_messages,
        "platforms": {
            item[0]: item[1]
            for item in platforms
        }
    }
