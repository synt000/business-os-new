from sqlalchemy.orm import Session
from datetime import datetime
import json

from .models import WelcomeSetting


class WelcomeService:

    @staticmethod
    def get_welcome(db: Session, language="mm"):

        data = (
            db.query(WelcomeSetting)
            .filter(
                WelcomeSetting.language == language
            )
            .first()
        )

        if not data:
            data = WelcomeSetting(
                id="default-"+language,
                language=language,
                title="Business OS",
                subtitle="All-in-One Business Management System",
                hero_message="မြန်မာလုပ်ငန်းများအတွက် Digital Business Platform",
                faq_content="FAQ Content",
                features_json=json.dumps([
                    "📦 Inventory Management",
                    "🛒 POS & Sales",
                    "💰 Finance Tracking",
                    "📊 Reports & Analytics",
                    "🤖 AI Business Assistant"
                ]),
                button_text="Continue",
                live_banner="Welcome to Business OS",
                banner_active=True
            )

        try:
            data.features_json = json.loads(
                data.features_json or "[]"
            )
        except:
            data.features_json = []

        try:
            data.sections_json = json.loads(
                data.sections_json or "[]"
            )
        except:
            data.sections_json = []

        if data.logo_url is None:
            data.logo_url = ""

        if data.hero_image_url is None:
            data.hero_image_url = ""

        if data.sections_json is None:
            data.sections_json = []

        if data.seo_title is None:
            data.seo_title = ""

        if data.seo_description is None:
            data.seo_description = ""

        data.logo_url = data.logo_url or ""
        data.hero_image_url = data.hero_image_url or ""
        data.seo_title = data.seo_title or ""
        data.seo_description = data.seo_description or ""

        if not data.sections_json:
            data.sections_json = []

        return data


    @staticmethod
    def update_welcome(
        db: Session,
        payload
    ):

        data = (
            db.query(WelcomeSetting)
            .filter(
                WelcomeSetting.language == payload.language
            )
            .first()
        )

        if not data:
            data = WelcomeSetting(
                id="welcome-"+payload.language,
                language=payload.language
            )
            db.add(data)


        data.title = payload.title
        data.subtitle = payload.subtitle
        data.hero_message = payload.hero_message
        data.faq_content = payload.faq_content

        data.features_json = json.dumps(
            payload.features_json or []
        )

        data.sections_json = json.dumps(
            payload.sections_json or []
        )

        data.button_text = payload.button_text
        data.live_banner = payload.live_banner
        data.banner_active = payload.banner_active

        data.logo_url = payload.logo_url or ""
        data.hero_image_url = payload.hero_image_url or ""
        data.theme_color = payload.theme_color or "#2563eb"

        data.seo_title = payload.seo_title or ""
        data.seo_description = payload.seo_description or ""

        data.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(data)

        try:
            data.features_json = json.loads(
                data.features_json or "[]"
            )
        except:
            data.features_json = []

        try:
            data.sections_json = json.loads(
                data.sections_json or "[]"
            )
        except:
            data.sections_json = []

        if data.logo_url is None:
            data.logo_url = ""

        if data.hero_image_url is None:
            data.hero_image_url = ""

        if data.sections_json is None:
            data.sections_json = []

        if data.seo_title is None:
            data.seo_title = ""

        if data.seo_description is None:
            data.seo_description = ""

        return data
