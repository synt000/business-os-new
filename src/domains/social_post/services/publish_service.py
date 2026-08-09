from datetime import datetime

from sqlalchemy.orm import Session

from src.models.saas_core import generate_uuid
from src.domains.social_center.models import SocialChannel
from src.domains.social_post.models import SocialPost
from src.domains.social_post.schemas import SocialPostCreate
from src.domains.social_post.publish_log_models import SocialPublishLog
from src.domains.social_post.adapters.factory import SocialPublisherFactory


class SocialPostPublishService:
    @staticmethod
    def create(
        db: Session,
        payload: SocialPostCreate,
    ):
        post = SocialPost(
            tenant_id=payload.tenant_id,
            channel_id=payload.channel_id,
            platform=payload.platform,
            content=payload.content,
            media_url=payload.media_url,
            scheduled_at=payload.scheduled_at,
            created_by=payload.created_by,
            status="draft",
        )

        db.add(post)
        db.commit()
        db.refresh(post)

        return post

    @staticmethod
    def list_by_tenant(
        db: Session,
        tenant_id: str,
    ):
        return (
            db.query(SocialPost)
            .filter(
                SocialPost.tenant_id == tenant_id,
            )
            .order_by(
                SocialPost.created_at.desc(),
            )
            .all()
        )

    @staticmethod
    def publish(
        db: Session,
        post_id: str,
    ):
        post = (
            db.query(SocialPost)
            .filter(
                SocialPost.id == post_id,
            )
            .first()
        )

        if not post:
            return None

        channel = (
            db.query(SocialChannel)
            .filter(
                SocialChannel.id == post.channel_id,
                SocialChannel.tenant_id == post.tenant_id,
                SocialChannel.is_active.is_(True),
            )
            .first()
        )

        if not channel:
            return None

        adapter = SocialPublisherFactory.get_adapter(
            post.platform,
        )

        channel_config = {
            "external_id": channel.external_id,
            "access_token": channel.access_token,
            "webhook_token": channel.webhook_token,
        }

        result = adapter.publish(
            content=post.content,
            media_url=post.media_url,
            channel_config=channel_config,
        )

        log = SocialPublishLog(
            id=generate_uuid(),
            post_id=post.id,
            channel_id=post.channel_id,
            platform=post.platform,
            success=bool(result and result.get("success")),
            response=str(result),
            created_at=datetime.utcnow(),
        )

        db.add(log)

        if result and result.get("success"):
            post.status = "published"
            post.published_at = datetime.utcnow()

        db.commit()
        db.refresh(post)

        return post
