from src.domains.social_post.adapters.facebook import (
    FacebookPublisherAdapter,
)

from src.domains.social_post.adapters.telegram import (
    TelegramPublisherAdapter,
)

from src.domains.social_post.adapters.instagram import (
    InstagramPublisherAdapter,
)

from src.domains.social_post.adapters.tiktok import (
    TikTokPublisherAdapter,
)


class SocialPublisherFactory:

    @staticmethod
    def get_adapter(platform: str):

        platform = platform.lower()

        if platform == "facebook":
            return FacebookPublisherAdapter()

        if platform == "telegram":
            return TelegramPublisherAdapter()

        if platform == "instagram":
            return InstagramPublisherAdapter()

        if platform == "tiktok":
            return TikTokPublisherAdapter()

        raise ValueError(
            f"Unsupported social platform: {platform}"
        )
