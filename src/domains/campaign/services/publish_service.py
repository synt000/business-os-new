import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from src.domains.campaign.models import Campaign, CampaignChannel
from src.domains.social_center.models import SocialChannel
from src.domains.social_post.models import SocialPost
from src.domains.social_post.publish_log_models import SocialPublishLog
from src.domains.social_post.adapters.factory import SocialPublisherFactory


class CampaignPublishService:

    @staticmethod
    def publish(db: Session, campaign_id: str):

        campaign = (
            db.query(Campaign)
            .filter(Campaign.id == campaign_id)
            .first()
        )

        if not campaign:
            return {
                "status": "NOT_FOUND",
                "message": "Campaign not found"
            }

        # Create social post first because publish logs require social_posts.id
        first_channel = (
            db.query(SocialChannel)
            .join(
                CampaignChannel,
                CampaignChannel.channel_id == SocialChannel.id
            )
            .filter(
                CampaignChannel.campaign_id == campaign_id
            )
            .first()
        )

        if not first_channel:
            return {
                "status": "NO_CHANNEL",
                "message": "Campaign has no linked social channel"
            }

        post = SocialPost(
            id=str(uuid.uuid4()),
            tenant_id=campaign.tenant_id,
            campaign_id=campaign.id,
            platform=first_channel.platform,
            channel_id=first_channel.id,
            content=campaign.content,
            status="published",
            created_at=datetime.utcnow()
        )

        db.add(post)
        db.flush()

        links = (
            db.query(CampaignChannel)
            .filter(
                CampaignChannel.campaign_id == campaign_id
            )
            .all()
        )

        results = []

        for link in links:

            channel = (
                db.query(SocialChannel)
                .filter(
                    SocialChannel.id == link.channel_id
                )
                .first()
            )

            if not channel:
                continue

            success = True
            response = {}

            if channel.platform in [
                "facebook",
                "telegram",
                "instagram",
                "tiktok"
            ]:
                adapter = SocialPublisherFactory.get_adapter(
                    channel.platform
                )

                if channel.platform == "telegram":
                    response = adapter.publish(
                        content=campaign.content,
                        media_url=None,
                        channel_config={
                            "chat_id": channel.external_id
                        }
                    )
                else:
                    response = adapter.publish(
                        content=campaign.content,
                        media_url=None
                    )

                success = response.get(
                    "success",
                    False
                )

            log = SocialPublishLog(
                id=str(uuid.uuid4()),
                post_id=post.id,
                channel_id=channel.id,
                platform=channel.platform,
                success=success,
                response=str(response),
                created_at=datetime.utcnow()
            )

            db.add(log)

            results.append(response)

        campaign.status = "published"

        db.commit()

        return {
            "campaign_id": campaign.id,
            "post_id": post.id,
            "status": "published",
            "results": results
        }
