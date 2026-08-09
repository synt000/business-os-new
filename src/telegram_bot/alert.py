import os
import requests
from dotenv import load_dotenv

load_dotenv(".env")

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CEO_CHAT_ID = os.getenv("TELEGRAM_CEO_CHAT_ID")


def send_ceo_alert(message: str) -> bool:
    """
    Send a synchronous Telegram alert to the configured CEO chat.
    Safe to call from the campaign scheduler/retry worker.
    """

    if not BOT_TOKEN:
        print("[Telegram Alert] TELEGRAM_BOT_TOKEN missing")
        return False

    if not CEO_CHAT_ID:
        print("[Telegram Alert] TELEGRAM_CEO_CHAT_ID missing")
        return False

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    try:
        response = requests.post(
            url,
            json={
                "chat_id": CEO_CHAT_ID,
                "text": message,
            },
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        if not data.get("ok"):
            print("[Telegram Alert] API rejected message:", data)
            return False

        print("[Telegram Alert] CEO alert sent")
        return True

    except Exception as e:
        print("[Telegram Alert] FAILED:", str(e))
        return False
