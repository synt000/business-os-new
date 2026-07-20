from pathlib import Path

p = Path("src/domains/social_center/service.py")

s = p.read_text()

start = s.index("def link_social_messages_to_customers(")

new_func = '''
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
                    platform=message.platform,
                    message_id=message.id,
                    status="NEW"
                )

                db.add(lead)
                leads += 1

    db.commit()

    return {
        "processed": len(messages),
        "linked": linked,
        "leads_created": leads
    }
'''

s = s[:start] + new_func + "\n"

p.write_text(s)
