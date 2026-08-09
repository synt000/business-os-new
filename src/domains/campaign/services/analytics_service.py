import ast
import json

from sqlalchemy.orm import Session

from src.domains.campaign.models import Campaign
from src.domains.social_post.publish_log_models import SocialPublishLog
from src.domains.social_post.models import SocialPost


class CampaignAnalyticsService:

    @staticmethod
    def get_campaign_analytics(
        db: Session,
        campaign_id: str
    ):

        campaign = (
            db.query(Campaign)
            .filter(
                Campaign.id == campaign_id
            )
            .first()
        )

        if not campaign:
            return {
                "status": "NOT_FOUND",
                "message": "Campaign not found"
            }

        posts = (
            db.query(SocialPost)
            .filter(
                SocialPost.campaign_id == campaign.id
            )
            .all()
        )

        post_ids = [
            p.id for p in posts
        ]

        logs = (
            db.query(SocialPublishLog)
            .filter(
                SocialPublishLog.post_id.in_(post_ids)
            )
            .all()
            if post_ids
            else []
        )

        total = len(logs)

        success_count = len(
            [
                l for l in logs
                if l.success
            ]
        )

        channels = []

        for l in logs:
            if isinstance(l.response, str):
                try:
                    response = json.loads(l.response)
                except Exception:
                    try:
                        response = ast.literal_eval(l.response)
                    except Exception:
                        response = l.response
            else:
                response = l.response

            channels.append(
                {
                    "platform": l.platform,
                    "success": l.success,
                    "response": response
                }
            )

        return {
            "campaign_id": campaign.id,
            "campaign_name": campaign.name,
            "status": campaign.status,
            "total_sent": total,
            "success_count": success_count,
            "failed_count": total - success_count,
            "success_rate":
                f"{round((success_count / total) * 100, 2)}%"
                if total else "0%",
            "channels": channels
        }
