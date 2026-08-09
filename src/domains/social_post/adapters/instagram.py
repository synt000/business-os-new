from src.domains.social_post.adapters.base import (
    SocialPublisherAdapter,
)


class InstagramPublisherAdapter(
    SocialPublisherAdapter
):

    def publish(
        self,
        content: str,
        media_url: str | None = None,
        channel_config: dict | None = None,
    ):
        # Future:
        # Instagram Graph API integration here

        return {
            "platform": "instagram",
            "success": True,
            "message": "Instagram publish simulated",
            "content": content,
            "media_url": media_url,
        }
