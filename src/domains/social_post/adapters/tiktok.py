from src.domains.social_post.adapters.base import (
    SocialPublisherAdapter,
)


class TikTokPublisherAdapter(
    SocialPublisherAdapter
):

    def publish(
        self,
        content: str,
        media_url: str | None = None,
        channel_config: dict | None = None,
    ):
        # Future:
        # TikTok Content Posting API integration

        return {
            "platform": "tiktok",
            "success": True,
            "message": "TikTok publish simulated",
            "content": content,
            "media_url": media_url,
        }
