import uuid

from sqlalchemy.orm import Session

from src.models.saas_core import (
    BusinessProfile,
    SocialAccount,
    SocialMessage,
    SocialLead
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


# ======================================
# SOCIAL MESSAGE INBOX
# ======================================

def get_social_messages(
    db: Session,
    tenant_id: str,
    limit: int = 50
):

    return (
        db.query(SocialMessage)
        .filter(
            SocialMessage.tenant_id == tenant_id
        )
        .order_by(
            SocialMessage.created_at.desc()
        )
        .limit(limit)
        .all()
    )



# ======================================
# SOCIAL MESSAGE CUSTOMER LINKER
# ======================================

from src.domains.social.services.customer_matcher import find_customer_match



def link_social_messages_to_customers(
    db: Session,
    tenant_id: str
):
    messages = (
        db.query(SocialMessage)
        .filter(
            SocialMessage.tenant_id == tenant_id,
            SocialMessage.customer_id == None
        )
        .all()
    )

    linked = 0
    leads = 0

    for message in messages:

        customer = find_customer_match(
            db=db,
            tenant_id=tenant_id,
            customer_name=message.customer_name
        )

        if customer:
            message.customer_id = customer.id
            linked += 1

        else:
            existing = (
                db.query(SocialLead)
                .filter(
                    SocialLead.message_id == message.id
                )
                .first()
            )

            if not existing:
                lead = SocialLead(
                    id=str(uuid.uuid4()),
                    customer_name=message.customer_name,
                    customer_phone=None,
                    platform=message.platform,
                    message_id=message.id,
                    status="NEW",
                    tenant_id=tenant_id
                )

                db.add(lead)
                leads += 1

    db.commit()

    return {
        "processed": len(messages),
        "linked": linked,
        "leads_created": leads
    }



# ======================================
# SOCIAL LEADS
# ======================================

def get_social_leads(
    db: Session,
    tenant_id: str,
    limit: int = 50
):
    return (
        db.query(SocialLead)
        .filter(
            SocialLead.tenant_id == tenant_id
        )
        .order_by(
            SocialLead.created_at.desc()
        )
        .limit(limit)
        .all()
    )


# ======================================
# SOCIAL LEAD STATUS UPDATE
# ======================================

from src.models.saas_core import SocialLead


def update_social_lead_status(
    db: Session,
    tenant_id: str,
    lead_id: str,
    status: str
):
    lead = (
        db.query(SocialLead)
        .filter(
            SocialLead.id == lead_id,
            SocialLead.tenant_id == tenant_id
        )
        .first()
    )

    if not lead:
        return None

    lead.status = status

    db.commit()
    db.refresh(lead)

    return lead


# ======================================
# SOCIAL LEAD STATUS UPDATE
# ======================================

from src.models.saas_core import SocialLead


def update_social_lead_status(
    db: Session,
    tenant_id: str,
    lead_id: str,
    status: str
):
    lead = (
        db.query(SocialLead)
        .filter(
            SocialLead.id == lead_id,
            SocialLead.tenant_id == tenant_id
        )
        .first()
    )

    if not lead:
        return None

    lead.status = status

    db.commit()
    db.refresh(lead)

    return lead
