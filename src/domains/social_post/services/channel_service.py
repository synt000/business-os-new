from sqlalchemy.orm import Session
from src.domains.social_post.channel_models import SocialChannel


class SocialChannelService:

    @staticmethod
    def create(
        db: Session,
        payload
    ):
        channel = SocialChannel(
            tenant_id=payload.tenant_id,
            platform=payload.platform,
            channel_name=payload.channel_name,
            external_id=payload.external_id,
            is_active=True
        )

        db.add(channel)
        db.commit()
        db.refresh(channel)

        return channel


    @staticmethod
    def list_by_tenant(
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
