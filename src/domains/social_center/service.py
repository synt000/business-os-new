from sqlalchemy.orm import Session

from src.domains.social_center.models import SocialChannel
from src.models.saas_core import SocialMessage, SocialMessageReply


class SocialCenterService:


    @staticmethod
    def list_channels(
        db: Session,
        tenant_id: str
    ):

        return (
            db.query(SocialChannel)
            .filter(
                SocialChannel.tenant_id == tenant_id
            )
            .all()
        )


    @staticmethod
    def save_message(
        db: Session,
        tenant_id: str,
        platform: str,
        customer_name: str,
        customer_id: str,
        message: str
    ):

        import uuid

        msg = SocialMessage(
            id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            platform=platform,
            customer_name=customer_name,
            customer_id=customer_id,
            message=message,
            message_type="text",
            status="unread"
        )

        db.add(msg)
        db.commit()
        db.refresh(msg)

        return msg


    @staticmethod
    def list_messages(
        db: Session,
        tenant_id: str
    ):

        return (
            db.query(SocialMessage)
            .filter(
                SocialMessage.tenant_id == tenant_id
            )
            .order_by(
                SocialMessage.created_at.desc()
            )
            .all()
        )


    @staticmethod
    def unread_messages(
        db: Session,
        tenant_id: str
    ):

        return (
            db.query(SocialMessage)
            .filter(
                SocialMessage.tenant_id == tenant_id,
                SocialMessage.status == "unread"
            )
            .order_by(
                SocialMessage.created_at.desc()
            )
            .all()
        )


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

        import uuid

        msg.reply_text = reply_text
        msg.status = "replied"

        reply = SocialMessageReply(
            id=str(uuid.uuid4()),
            message_id=message_id,
            tenant_id=tenant_id,
            reply_text=reply_text,
            replied_by="admin"
        )

        db.add(reply)

        db.commit()

        db.refresh(reply)

        return {
            "message": msg,
            "reply_id": reply.id
        }





    @staticmethod
    def mark_read(
        db: Session,
        tenant_id: str,
        customer_id: str
    ):

        messages = (
            db.query(SocialMessage)
            .filter(
                SocialMessage.tenant_id == tenant_id,
                SocialMessage.customer_id == customer_id,
                SocialMessage.status == "unread"
            )
            .all()
        )

        for msg in messages:
            msg.status = "read"

        db.commit()

        return {
            "updated": len(messages)
        }



    @staticmethod
    def customer_profile(
        db: Session,
        tenant_id: str,
        customer_id: str
    ):

        messages = (
            db.query(SocialMessage)
            .filter(
                SocialMessage.tenant_id == tenant_id,
                SocialMessage.customer_id == customer_id
            )
            .order_by(
                SocialMessage.created_at.desc()
            )
            .all()
        )


        if not messages:
            return {
                "customer_id": customer_id,
                "name": "-",
                "platform": "-",
                "total_messages": 0,
                "last_seen": None,
                "tags": []
            }


        latest = messages[0]


        return {
            "customer_id": customer_id,
            "name": latest.customer_name,
            "platform": latest.platform,
            "total_messages": len(messages),
            "last_seen": latest.created_at,
            "tags": [
                "New Lead"
            ]
        }


    @staticmethod
    def get_conversation(
        db: Session,
        tenant_id: str,
        customer_id: str
    ):

        messages = (
            db.query(SocialMessage)
            .filter(
                SocialMessage.tenant_id == tenant_id,
                SocialMessage.customer_id == customer_id
            )
            .order_by(
                SocialMessage.created_at.asc()
            )
            .all()
        )

        history = []

        for msg in messages:

            history.append({
                "type": "incoming",
                "message_id": msg.id,
                "text": msg.message,
                "customer_name": msg.customer_name,
                "attachments": [
                    {
                        "url": a.file_url,
                        "name": a.file_name,
                        "type": a.file_type
                    }
                    for a in db.query(
                        __import__(
                            "src.models.saas_core",
                            fromlist=["SocialMessageAttachment"]
                        ).SocialMessageAttachment
                    ).filter(
                        __import__(
                            "src.models.saas_core",
                            fromlist=["SocialMessageAttachment"]
                        ).SocialMessageAttachment.message_id == msg.id,
                        __import__(
                            "src.models.saas_core",
                            fromlist=["SocialMessageAttachment"]
                        ).SocialMessageAttachment.tenant_id == tenant_id
                    ).all()
                ],

                  "attachment_url": (
                      (
                          db.query(
                              __import__(
                                  "src.models.saas_core",
                                  fromlist=["SocialMessageAttachment"]
                              ).SocialMessageAttachment
                          )
                          .filter(
                              __import__(
                                  "src.models.saas_core",
                                  fromlist=["SocialMessageAttachment"]
                              ).SocialMessageAttachment.message_id == msg.id,
                              __import__(
                                  "src.models.saas_core",
                                  fromlist=["SocialMessageAttachment"]
                              ).SocialMessageAttachment.tenant_id == tenant_id
                          )
                          .first()
                      ).file_url
                      if db.query(
                          __import__(
                              "src.models.saas_core",
                              fromlist=["SocialMessageAttachment"]
                          ).SocialMessageAttachment
                      ).filter(
                          __import__(
                              "src.models.saas_core",
                              fromlist=["SocialMessageAttachment"]
                          ).SocialMessageAttachment.message_id == msg.id,
                          __import__(
                              "src.models.saas_core",
                              fromlist=["SocialMessageAttachment"]
                          ).SocialMessageAttachment.tenant_id == tenant_id
                      ).first()
                      else None
                  ),

                  "attachment_name": (
                      (
                          db.query(
                              __import__(
                                  "src.models.saas_core",
                                  fromlist=["SocialMessageAttachment"]
                              ).SocialMessageAttachment
                          )
                          .filter(
                              __import__(
                                  "src.models.saas_core",
                                  fromlist=["SocialMessageAttachment"]
                              ).SocialMessageAttachment.message_id == msg.id,
                              __import__(
                                  "src.models.saas_core",
                                  fromlist=["SocialMessageAttachment"]
                              ).SocialMessageAttachment.tenant_id == tenant_id
                          )
                          .first()
                      ).file_name
                      if db.query(
                          __import__(
                              "src.models.saas_core",
                              fromlist=["SocialMessageAttachment"]
                          ).SocialMessageAttachment
                      ).filter(
                          __import__(
                              "src.models.saas_core",
                              fromlist=["SocialMessageAttachment"]
                          ).SocialMessageAttachment.message_id == msg.id,
                          __import__(
                              "src.models.saas_core",
                              fromlist=["SocialMessageAttachment"]
                          ).SocialMessageAttachment.tenant_id == tenant_id
                      ).first()
                      else None
                  ),

                "time": msg.created_at
            })

            replies = (
                db.query(SocialMessageReply)
                .filter(
                    SocialMessageReply.message_id == msg.id,
                    SocialMessageReply.tenant_id == tenant_id
                )
                .order_by(
                    SocialMessageReply.created_at.asc()
                )
                .all()
            )

            for reply in replies:
                history.append({
                    "type": "reply",
                    "message_id": msg.id,
                    "text": reply.reply_text,
                    "replied_by": reply.replied_by,
                    "time": reply.created_at
                })

        return history


def get_social_summary(
    db: Session,
    tenant_id: str
):

    channels = (
        db.query(SocialChannel)
        .filter(
            SocialChannel.tenant_id == tenant_id
        )
        .count()
    )

    messages = (
        db.query(SocialMessage)
        .filter(
            SocialMessage.tenant_id == tenant_id
        )
        .count()
    )

    unread = (
        db.query(SocialMessage)
        .filter(
            SocialMessage.tenant_id == tenant_id,
            SocialMessage.status == "unread"
        )
        .count()
    )

    replied = (
        db.query(SocialMessage)
        .filter(
            SocialMessage.tenant_id == tenant_id,
            SocialMessage.status == "replied"
        )
        .count()
    )

    return {
        "channels": channels,
        "messages": messages,
        "unread": unread,
        "replied": replied
    }


    @staticmethod
    def create_channel(
        db: Session,
        tenant_id: str,
        data
    ):
        import uuid

        channel = SocialChannel(
            id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            platform=data.platform,
            channel_name=data.channel_name,
            external_id=data.external_id,
            access_token=data.access_token,
            webhook_token=data.webhook_token,
            is_active=True
        )

        db.add(channel)
        db.commit()
        db.refresh(channel)

        return channel
