import os
import requests

from src.domains.social_post.adapters.base import (
    SocialPublisherAdapter,
)


class TelegramPublisherAdapter(
    SocialPublisherAdapter
):

    def publish(
        self,
        content: str,
        media_url: str | None = None,
        channel_config: dict | None = None
    ):

        token = os.getenv("TELEGRAM_BOT_TOKEN")

        if not token:
            return {
                "platform": "telegram",
                "success": False,
                "message": "TELEGRAM_BOT_TOKEN missing",
            }

        if not channel_config:
            return {
                "platform": "telegram",
                "success": False,
                "message": "telegram channel config missing",
            }

        chat_id = channel_config.get("chat_id")

        if not chat_id:
            return {
                "platform": "telegram",
                "success": False,
                "message": "chat_id missing",
            }

        url = (
            f"https://api.telegram.org/"
            f"bot{token}/sendMessage"
        )

        payload = {
            "chat_id": chat_id,
            "text": content,
        }

        response = requests.post(
            url,
            json=payload,
            timeout=15
        )

        return {
            "platform": "telegram",
            "success": response.ok,
            "response": response.text,
        }
