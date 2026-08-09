from src.domains.social_post.adapters.base import (
    SocialPublisherAdapter,
)


class FacebookPublisherAdapter(
    SocialPublisherAdapter
):

    def publish(
        self,
        content: str,
        media_url: str | None = None,
        channel_config: dict | None = None,
    ):
        # Future:
        # Facebook Graph API call here

        return {
            "platform": "facebook",
            "success": True,
            "message": "Facebook publish simulated",
            "content": content,
            "media_url": media_url,
        }
