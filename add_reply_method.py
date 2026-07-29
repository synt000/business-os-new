from pathlib import Path

p = Path("src/domains/social_center/service.py")

s = p.read_text()

if "def update_reply(" in s:
    print("update_reply already exists")
    exit()

insert = '''

    @staticmethod
    def update_reply(
        db: Session,
        tenant_id: str,
        message_id: str,
        reply_text: str
    ):

        msg = (
            db.query(SocialMessage)
            .filter(
                SocialMessage.id == message_id,
                SocialMessage.tenant_id == tenant_id
            )
            .first()
        )

        if not msg:
            return None

        msg.reply_text = reply_text
        msg.status = "replied"

        db.commit()
        db.refresh(msg)

        return msg

'''

s = s + insert

p.write_text(s)

print("added update_reply")
